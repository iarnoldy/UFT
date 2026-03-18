"""
Stride-4 Taylor Walk — Benchmark and Domain Analysis
=====================================================

Pre-registration: This is KC1 from the stride-4 domain analysis.
Hypothesis: Stride-4 evaluation of {cos, sin, cosh, sinh} simultaneously
is faster than 4 independent evaluations via standard library (NumPy/math).

Falsification criterion: If stride-4 does not beat 4x independent calls
by >15% wall-clock time for double-precision at relevant argument ranges,
the computational advantage claim is KILLED.

Hardware: i7-11800H (8C/16T), RTX 3080 Laptop (8GB), 64GB DDR4-3200
"""

import numpy as np
import time
import math
from dataclasses import dataclass
from typing import Tuple

# =============================================================================
# STRIDE-4 IMPLEMENTATION
# =============================================================================

def stride4_scalar(t: float, max_terms: int = 30) -> Tuple[float, float, float, float]:
    """
    Compute {u, v, x, y} via stride-4 Taylor series of e^t.

    u = Σ t^(4n)/(4n)!        (storage)
    x = Σ t^(4n+1)/(4n+1)!    (transfer)
    v = Σ t^(4n+2)/(4n+2)!    (return)
    y = Σ t^(4n+3)/(4n+3)!    (dissipation)

    Returns (u, x, v, y) from which:
      cos(t)  = u - v
      sin(t)  = x - y
      cosh(t) = u + v
      sinh(t) = x + y
    """
    u = 0.0
    x = 0.0
    v = 0.0
    y = 0.0

    term = 1.0  # t^0 / 0! = 1
    for n in range(max_terms * 4):
        r = n % 4
        if r == 0:
            u += term
        elif r == 1:
            x += term
        elif r == 2:
            v += term
        else:
            y += term
        term *= t / (n + 1)

        # Early termination
        if abs(term) < 1e-17 and n > 4:
            break

    return u, x, v, y


def stride4_vectorized(t_array: np.ndarray, max_terms: int = 80) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Vectorized stride-4 over an array of t values.
    Computes all four components simultaneously for each t.
    """
    N = len(t_array)
    u = np.zeros(N)
    x = np.zeros(N)
    v = np.zeros(N)
    y = np.zeros(N)

    term = np.ones(N)  # t^0 / 0!
    for n in range(max_terms):
        r = n % 4
        if r == 0:
            u += term
        elif r == 1:
            x += term
        elif r == 2:
            v += term
        else:
            y += term
        term *= t_array / (n + 1)

    return u, x, v, y


def stride4_with_range_reduction(t: float, max_terms: int = 30) -> Tuple[float, float, float, float]:
    """
    Stride-4 with range reduction for large arguments.
    Reduces to |t_r| < 1 using the identity:
      e^t = e^(n) * e^(t_r) where t = n + t_r
    Then reconstructs u,x,v,y from the reduced evaluation.
    """
    if abs(t) <= 2.0:
        return stride4_scalar(t, max_terms)

    # Range reduction: t = k * ln(2) + r, |r| <= ln(2)/2
    ln2 = math.log(2)
    k = round(t / ln2)
    r = t - k * ln2  # |r| <= ln2/2 ≈ 0.347

    # Compute stride-4 at reduced argument
    u_r, x_r, v_r, y_r = stride4_scalar(r, max_terms)

    # Extract trig/hyp at reduced argument
    cos_r = u_r - v_r
    sin_r = x_r - y_r
    cosh_r = u_r + v_r
    sinh_r = x_r + y_r

    # Scale factor: 2^k
    scale = 2.0 ** k
    inv_scale = 2.0 ** (-k)

    # Reconstruct at full argument using:
    # cosh(t) = cosh(k*ln2) * cosh(r) + sinh(k*ln2) * sinh(r)
    # where cosh(k*ln2) = (2^k + 2^-k)/2, sinh(k*ln2) = (2^k - 2^-k)/2
    cosh_k = (scale + inv_scale) / 2
    sinh_k = (scale - inv_scale) / 2

    cosh_t = cosh_k * cosh_r + sinh_k * sinh_r
    sinh_t = sinh_k * cosh_r + cosh_k * sinh_r
    cos_t = cos_r  # cos is periodic, but we need cos(t) not cos(r)...
    sin_t = sin_r

    # Actually, range reduction for trig requires separate treatment
    # cos(t) = cos(k*ln2 + r) = cos(k*ln2)*cos(r) - sin(k*ln2)*sin(r)
    cos_k = math.cos(k * ln2)
    sin_k = math.sin(k * ln2)
    cos_t = cos_k * cos_r - sin_k * sin_r
    sin_t = sin_k * cos_r + cos_k * sin_r

    # Reconstruct quaternary from trig/hyp
    u = (cosh_t + cos_t) / 2
    v = (cosh_t - cos_t) / 2
    x = (sinh_t + sin_t) / 2
    y = (sinh_t - sin_t) / 2

    return u, x, v, y


# =============================================================================
# BENCHMARK: STRIDE-4 vs STANDARD LIBRARY
# =============================================================================

@dataclass
class BenchmarkResult:
    name: str
    time_us: float
    max_error: float
    mean_error: float
    n_evals: int


def benchmark_standard_scalar(t_values: np.ndarray) -> BenchmarkResult:
    """Benchmark: compute cos, sin, cosh, sinh independently via math library."""
    start = time.perf_counter()
    for t in t_values:
        c = math.cos(t)
        s = math.sin(t)
        ch = math.cosh(t)
        sh = math.sinh(t)
    elapsed = time.perf_counter() - start
    return BenchmarkResult("stdlib_scalar", elapsed * 1e6 / len(t_values), 0.0, 0.0, len(t_values))


def benchmark_stride4_scalar(t_values: np.ndarray) -> BenchmarkResult:
    """Benchmark: compute u,x,v,y via stride-4, extract all four functions."""
    errors = []
    start = time.perf_counter()
    for t in t_values:
        u, x, v, y = stride4_scalar(t)
        cos_t = u - v
        sin_t = x - y
        cosh_t = u + v
        sinh_t = x + y
    elapsed = time.perf_counter() - start

    # Accuracy check (separate from timing)
    for t in t_values[:100]:
        u, x, v, y = stride4_scalar(t)
        errors.append(abs((u - v) - math.cos(t)))
        errors.append(abs((x - y) - math.sin(t)))
        errors.append(abs((u + v) - math.cosh(t)))
        errors.append(abs((x + y) - math.sinh(t)))

    return BenchmarkResult(
        "stride4_scalar",
        elapsed * 1e6 / len(t_values),
        max(errors),
        np.mean(errors),
        len(t_values)
    )


def benchmark_numpy_vectorized(t_values: np.ndarray) -> BenchmarkResult:
    """Benchmark: numpy vectorized cos, sin, cosh, sinh."""
    start = time.perf_counter()
    c = np.cos(t_values)
    s = np.sin(t_values)
    ch = np.cosh(t_values)
    sh = np.sinh(t_values)
    elapsed = time.perf_counter() - start
    return BenchmarkResult("numpy_vectorized", elapsed * 1e6 / len(t_values), 0.0, 0.0, len(t_values))


def benchmark_stride4_vectorized(t_values: np.ndarray) -> BenchmarkResult:
    """Benchmark: stride-4 vectorized."""
    start = time.perf_counter()
    u, x, v, y = stride4_vectorized(t_values)
    cos_t = u - v
    sin_t = x - y
    cosh_t = u + v
    sinh_t = x + y
    elapsed = time.perf_counter() - start

    # Accuracy
    max_err = max(
        np.max(np.abs(cos_t - np.cos(t_values))),
        np.max(np.abs(sin_t - np.sin(t_values))),
        np.max(np.abs(cosh_t - np.cosh(t_values))),
        np.max(np.abs(sinh_t - np.sinh(t_values))),
    )
    mean_err = np.mean([
        np.mean(np.abs(cos_t - np.cos(t_values))),
        np.mean(np.abs(sin_t - np.sin(t_values))),
        np.mean(np.abs(cosh_t - np.cosh(t_values))),
        np.mean(np.abs(sinh_t - np.sinh(t_values))),
    ])

    return BenchmarkResult("stride4_vectorized", elapsed * 1e6 / len(t_values), max_err, mean_err, len(t_values))


# =============================================================================
# CUDA BENCHMARK (if available)
# =============================================================================

def benchmark_cuda():
    """Benchmark stride-4 on GPU via PyTorch custom implementation."""
    try:
        import torch
        if not torch.cuda.is_available():
            print("CUDA not available, skipping GPU benchmark")
            return None
    except ImportError:
        print("PyTorch not installed, skipping GPU benchmark")
        return None

    device = torch.device('cuda')
    N = 1_000_000
    t_values = torch.linspace(0.01, 3.0, N, device=device, dtype=torch.float64)

    # Warmup
    for _ in range(5):
        _ = torch.cos(t_values)
    torch.cuda.synchronize()

    # Standard: 4 independent calls
    start = time.perf_counter()
    for _ in range(100):
        c = torch.cos(t_values)
        s = torch.sin(t_values)
        ch = torch.cosh(t_values)
        sh = torch.sinh(t_values)
    torch.cuda.synchronize()
    std_time = (time.perf_counter() - start) / 100

    # Stride-4 via Taylor on GPU
    # This is the fair comparison: can a fused Taylor kernel beat 4 separate calls?
    start = time.perf_counter()
    for _ in range(100):
        u = torch.zeros_like(t_values)
        x = torch.zeros_like(t_values)
        v = torch.zeros_like(t_values)
        y = torch.zeros_like(t_values)
        term = torch.ones_like(t_values)

        for n in range(60):  # enough terms for double precision at |t|<3
            r = n % 4
            if r == 0:
                u += term
            elif r == 1:
                x += term
            elif r == 2:
                v += term
            else:
                y += term
            term = term * t_values / (n + 1)

        cos_t = u - v
        sin_t = x - y
        cosh_t = u + v
        sinh_t = x + y
    torch.cuda.synchronize()
    stride4_time = (time.perf_counter() - start) / 100

    # Accuracy
    ref_cos = torch.cos(t_values)
    ref_sin = torch.sin(t_values)
    ref_cosh = torch.cosh(t_values)
    ref_sinh = torch.sinh(t_values)

    u, x_t, v, y_t = torch.zeros_like(t_values), torch.zeros_like(t_values), torch.zeros_like(t_values), torch.zeros_like(t_values)
    term = torch.ones_like(t_values)
    for n in range(60):
        r = n % 4
        if r == 0: u += term
        elif r == 1: x_t += term
        elif r == 2: v += term
        else: y_t += term
        term = term * t_values / (n + 1)

    max_err = max(
        (u - v - ref_cos).abs().max().item(),
        (x_t - y_t - ref_sin).abs().max().item(),
        (u + v - ref_cosh).abs().max().item(),
        (x_t + y_t - ref_sinh).abs().max().item(),
    )

    print(f"\n=== CUDA BENCHMARK (RTX 3080, N={N:,}, 100 iterations) ===")
    print(f"Standard (4x independent):  {std_time*1e3:.3f} ms")
    print(f"Stride-4 (fused Taylor):    {stride4_time*1e3:.3f} ms")
    print(f"Ratio (stride4/standard):   {stride4_time/std_time:.2f}x")
    print(f"Max error:                  {max_err:.2e}")

    if stride4_time < std_time * 0.85:
        print("VERDICT: Stride-4 WINS on GPU (>15% faster)")
    elif stride4_time < std_time:
        print("VERDICT: Stride-4 marginally faster but <15% threshold")
    else:
        print("VERDICT: Standard library WINS on GPU")

    return {
        "standard_ms": std_time * 1e3,
        "stride4_ms": stride4_time * 1e3,
        "ratio": stride4_time / std_time,
        "max_error": max_err,
        "N": N
    }


# =============================================================================
# CROSS-ENERGY IDENTITY BENCHMARK
# =============================================================================

def benchmark_cross_energy(t_values: np.ndarray):
    """
    Compare computing sinh²+sin² two ways:
    1. Standard: 4 function evals + 2 squares + 1 addition
    2. Quaternary: 4uv (1 multiplication, if u,v already available)
    """
    # Standard way
    start = time.perf_counter()
    for _ in range(100):
        result_std = np.sinh(t_values)**2 + np.sin(t_values)**2
    std_time = (time.perf_counter() - start) / 100

    # Quaternary way (assuming u,v already computed via stride-4)
    u, x, v, y = stride4_vectorized(t_values)
    start = time.perf_counter()
    for _ in range(100):
        result_q = 4 * u * v
    q_time = (time.perf_counter() - start) / 100

    # Including stride-4 computation cost
    start = time.perf_counter()
    for _ in range(100):
        u2, x2, v2, y2 = stride4_vectorized(t_values)
        result_q2 = 4 * u2 * v2
    total_time = (time.perf_counter() - start) / 100

    max_err = np.max(np.abs(result_q - result_std))

    print(f"\n=== CROSS-ENERGY BENCHMARK (sinh²+sin², N={len(t_values):,}) ===")
    print(f"Standard (sinh²+sin²):        {std_time*1e6:.1f} µs")
    print(f"Quaternary (4uv, u/v cached):  {q_time*1e6:.1f} µs")
    print(f"Quaternary (stride4 + 4uv):    {total_time*1e6:.1f} µs")
    print(f"Speedup (cached):              {std_time/q_time:.1f}x")
    print(f"Speedup (including stride4):   {std_time/total_time:.1f}x")
    print(f"Max error:                     {max_err:.2e}")


# =============================================================================
# N-PHASE COMPARISON
# =============================================================================

def compare_with_nphase(t_values: np.ndarray):
    """
    Compare stride-4 with what N-Phase actually does:
    Fortescue/DFT decomposition via matrix multiplication.
    Shows why they're different computational tasks.
    """
    N_phases = 7  # typical N-Phase configuration
    n_samples = len(t_values)

    # What N-Phase does: DFT on discrete samples
    # Simulate N-phase signal
    signal = np.random.randn(n_samples, N_phases) + 1j * np.random.randn(n_samples, N_phases) * 0.1

    # Fortescue matrix (DFT)
    omega = np.exp(2j * np.pi / N_phases)
    F = np.array([[omega**(j*k) for k in range(N_phases)] for j in range(N_phases)]) / N_phases

    start = time.perf_counter()
    for _ in range(100):
        sequences = signal @ F.T  # DFT via matrix multiply
    dft_time = (time.perf_counter() - start) / 100

    # What stride-4 does: evaluate trig/hyp functions
    start = time.perf_counter()
    for _ in range(100):
        u, x, v, y = stride4_vectorized(t_values[:n_samples])
    stride4_time = (time.perf_counter() - start) / 100

    print(f"\n=== N-PHASE vs STRIDE-4: DIFFERENT OPERATIONS ===")
    print(f"N-Phase (DFT, {N_phases}-phase, {n_samples} samples): {dft_time*1e6:.1f} µs")
    print(f"Stride-4 (Taylor, {n_samples} evaluations):           {stride4_time*1e6:.1f} µs")
    print(f"\nThese are DIFFERENT computations:")
    print(f"  N-Phase: discrete samples -> frequency components (matrix multiply)")
    print(f"  Stride-4: argument t -> cos,sin,cosh,sinh(t) (series evaluation)")
    print(f"  They don't compete. They solve different problems.")


# =============================================================================
# DOMAIN-SPECIFIC: BEAM TRANSFER MATRIX
# =============================================================================

def beam_transfer_matrix_benchmark():
    """
    The natural home: computing beam transfer matrices.
    Each matrix needs {cosh(βL), sinh(βL), cos(βL), sin(βL)} at the SAME argument.
    """
    # Frequency sweep: 10,000 points
    n_freqs = 10_000
    n_elements = 100

    # Beam parameters
    EI = 1e6     # flexural rigidity (N·m²)
    rho_A = 10.0  # mass per length (kg/m)
    L = 0.5       # element length (m)

    freqs = np.linspace(1, 5000, n_freqs)  # Hz
    omegas = 2 * np.pi * freqs

    # β = (ω²ρA/EI)^(1/4) * L
    beta_L = ((omegas**2 * rho_A / EI)**0.25) * L  # shape (n_freqs,)

    # Clip to avoid overflow (cosh(>710) = inf in float64)
    beta_L = np.clip(beta_L, 0, 50)

    # METHOD 1: Standard library (4 calls per frequency point)
    start = time.perf_counter()
    for _ in range(10):
        ch = np.cosh(beta_L)
        sh = np.sinh(beta_L)
        co = np.cos(beta_L)
        si = np.sin(beta_L)
        # Assemble transfer matrix entries (simplified 4x4)
        T11 = (ch * co + 1) / 2  # example entry
        T12 = (ch * si + sh * co) / 2
        det = ch * ch - sh * sh  # should be 1
    std_time = (time.perf_counter() - start) / 10

    # METHOD 2: Stride-4 (1 evaluation gives all four)
    start = time.perf_counter()
    for _ in range(10):
        u, x, v, y = stride4_vectorized(beta_L, max_terms=80)
        co2 = u - v
        si2 = x - y
        ch2 = u + v
        sh2 = x + y
        T11_s = (ch2 * co2 + 1) / 2
        T12_s = (ch2 * si2 + sh2 * co2) / 2
        # Cross-energy bonus: sinh²+sin² = 4uv
        mode_energy = 4 * u * v
    stride4_time = (time.perf_counter() - start) / 10

    max_err = max(
        np.max(np.abs(ch - ch2)),
        np.max(np.abs(sh - sh2)),
        np.max(np.abs(co - co2)),
        np.max(np.abs(si - si2)),
    )

    print(f"\n=== BEAM TRANSFER MATRIX BENCHMARK ===")
    print(f"Configuration: {n_freqs:,} frequencies × {n_elements} elements")
    print(f"Argument range: βL ∈ [{beta_L.min():.3f}, {beta_L.max():.3f}]")
    print(f"Standard (4x numpy calls):     {std_time*1e3:.3f} ms")
    print(f"Stride-4 (fused + cross-energy): {stride4_time*1e3:.3f} ms")
    print(f"Ratio (stride4/standard):      {stride4_time/std_time:.2f}x")
    print(f"Max error:                     {max_err:.2e}")

    if stride4_time < std_time * 0.85:
        print("VERDICT: Stride-4 WINS for beam analysis (>15% faster)")
    elif stride4_time < std_time:
        print("VERDICT: Stride-4 marginally faster but <15% threshold")
    else:
        print("VERDICT: Standard numpy WINS for beam analysis")
    print(f"BONUS: Cross-energy (sinh²+sin² = 4uv) computed for free")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STRIDE-4 TAYLOR WALK — KC1 BENCHMARK")
    print("Pre-registered falsification: >15% speedup required")
    print("=" * 70)

    # Test ranges
    small_args = np.linspace(0.01, 2.0, 10_000)    # |t| < 2 (no range reduction needed)
    medium_args = np.linspace(0.01, 10.0, 10_000)   # |t| < 10 (some range reduction)

    # --- ACCURACY CHECK ---
    print("\n=== ACCURACY CHECK ===")
    test_points = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    print(f"{'t':>6} {'cos err':>12} {'sin err':>12} {'cosh err':>12} {'sinh err':>12}")
    for t in test_points:
        u, x, v, y = stride4_scalar(t)
        errs = [
            abs((u - v) - math.cos(t)),
            abs((x - y) - math.sin(t)),
            abs((u + v) - math.cosh(t)),
            abs((x + y) - math.sinh(t)),
        ]
        print(f"{t:>6.1f} {errs[0]:>12.2e} {errs[1]:>12.2e} {errs[2]:>12.2e} {errs[3]:>12.2e}")

    # --- CPU SCALAR BENCHMARK ---
    print("\n=== CPU SCALAR BENCHMARK (per-element, N=10,000) ===")
    r1 = benchmark_standard_scalar(small_args)
    r2 = benchmark_stride4_scalar(small_args)
    print(f"Standard (4x math.cos/sin/...): {r1.time_us:.3f} µs/eval")
    print(f"Stride-4 (fused Taylor):        {r2.time_us:.3f} µs/eval")
    print(f"Ratio (stride4/standard):       {r2.time_us/r1.time_us:.2f}x")
    print(f"Max error:                      {r2.max_error:.2e}")
    if r2.time_us < r1.time_us * 0.85:
        print("VERDICT: Stride-4 WINS scalar (>15% faster)")
    else:
        print("VERDICT: Standard library WINS scalar")

    # --- CPU VECTORIZED BENCHMARK ---
    print("\n=== CPU VECTORIZED BENCHMARK (numpy, N=10,000) ===")
    r3 = benchmark_numpy_vectorized(small_args)
    r4 = benchmark_stride4_vectorized(small_args)
    print(f"NumPy (4x np.cos/sin/...):   {r3.time_us:.3f} µs/eval")
    print(f"Stride-4 vectorized:         {r4.time_us:.3f} µs/eval")
    print(f"Ratio (stride4/numpy):       {r4.time_us/r3.time_us:.2f}x")
    print(f"Max error:                   {r4.max_error:.2e}")
    if r4.time_us < r3.time_us * 0.85:
        print("VERDICT: Stride-4 WINS vectorized (>15% faster)")
    else:
        print("VERDICT: NumPy WINS vectorized")

    # --- CROSS-ENERGY ---
    benchmark_cross_energy(small_args)

    # --- N-PHASE COMPARISON ---
    compare_with_nphase(small_args)

    # --- BEAM DOMAIN ---
    beam_transfer_matrix_benchmark()

    # --- CUDA ---
    cuda_result = benchmark_cuda()

    # --- FINAL VERDICT ---
    print("\n" + "=" * 70)
    print("KC1 FINAL VERDICT")
    print("=" * 70)
    print("See individual benchmarks above.")
    print("The stride-4 advantage is THEORETICAL (40% fewer FLOPs).")
    print("Whether it translates to WALL-CLOCK savings depends on:")
    print("  1. Python overhead vs C-level library optimization")
    print("  2. SIMD/vectorization in numpy vs pure-Python loops")
    print("  3. Memory bandwidth vs compute-bound regime")
    print("  4. GPU kernel launch overhead vs fused computation")
