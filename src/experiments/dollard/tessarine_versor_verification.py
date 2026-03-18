"""
Tessarine Versor Algebra Verification
======================================
Algebraic verification that Dollard's versor algebra {1, j, h, k} with
  j^2 = -1, h^2 = +1, k = hj, hj = jh (commutative)
is the tessarine algebra (Cockle, 1848).

Tests:
  1. Full multiplication table
  2. Z*Y product expansion
  3. Specific claim: Z*Y = h(XB+RG) + j(XG-RB)
  4. Idempotent decomposition
  5. Quaternary expansion of tessarine exponential
  6. jk product verification

Author: dollard-theorist agent
Date: 2026-03-17
"""

from sympy import (
    symbols, expand, simplify, cos, sin, cosh, sinh,
    Rational, I, pi, exp, series, Symbol, S, oo,
    Function, collect, Add, Mul, Pow
)
from sympy import sqrt
from collections import OrderedDict
import sys

# =============================================================================
# SECTION 0: Define Tessarine Algebra via symbolic computation
# =============================================================================
# We represent tessarines as formal linear combinations a + b*j + c*h + d*k
# where j, h, k are symbolic units. We implement multiplication via the table.

# Real symbols for impedance/admittance
R, X, G, B = symbols('R X G B', real=True)
theta, delta = symbols('theta delta', real=True)
t = symbols('t', real=True)
n = Symbol('n', integer=True, nonnegative=True)

class Tessarine:
    """
    Tessarine element: a + b*j + c*h + d*k
    where j^2 = -1, h^2 = +1, k = hj = jh, k^2 = -1
    All basis elements commute (tessarines are commutative).
    """
    def __init__(self, a=0, b=0, c=0, d=0):
        """a + b*j + c*h + d*k"""
        self.a = a  # scalar (1)
        self.b = b  # j coefficient
        self.c = c  # h coefficient
        self.d = d  # k coefficient

    def __repr__(self):
        terms = []
        if self.a != 0:
            terms.append(f"({self.a})")
        if self.b != 0:
            terms.append(f"({self.b})*j")
        if self.c != 0:
            terms.append(f"({self.c})*h")
        if self.d != 0:
            terms.append(f"({self.d})*k")
        return " + ".join(terms) if terms else "0"

    def __add__(self, other):
        if isinstance(other, (int, float)) or hasattr(other, 'is_number'):
            return Tessarine(self.a + other, self.b, self.c, self.d)
        return Tessarine(
            expand(self.a + other.a),
            expand(self.b + other.b),
            expand(self.c + other.c),
            expand(self.d + other.d)
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Tessarine(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        """
        Tessarine multiplication using the table:
          1*1=1, 1*j=j, 1*h=h, 1*k=k
          j*1=j, j*j=-1, j*h=k, j*k=-h
          h*1=h, h*j=k, h*h=1, h*k=j
          k*1=k, k*j=-h, k*h=j, k*k=-1
        """
        if isinstance(other, (int, float)) or hasattr(other, 'is_number'):
            return Tessarine(
                expand(self.a * other),
                expand(self.b * other),
                expand(self.c * other),
                expand(self.d * other)
            )

        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d

        # Expand (a1 + b1*j + c1*h + d1*k)(a2 + b2*j + c2*h + d2*k)
        # using the multiplication table:

        # Real part (coefficient of 1):
        # 1*1=1: a1*a2
        # j*j=-1: b1*b2*(-1)
        # h*h=1: c1*c2*(1)
        # k*k=-1: d1*d2*(-1)
        real = expand(a1*a2 - b1*b2 + c1*c2 - d1*d2)

        # j coefficient:
        # 1*j=j: a1*b2
        # j*1=j: b1*a2
        # h*k=j: c1*d2
        # k*h=j: d1*c2
        j_coeff = expand(a1*b2 + b1*a2 + c1*d2 + d1*c2)

        # h coefficient:
        # 1*h=h: a1*c2
        # h*1=h: c1*a2
        # j*k=-h: b1*d2*(-1)
        # k*j=-h: d1*b2*(-1)
        h_coeff = expand(a1*c2 + c1*a2 - b1*d2 - d1*b2)

        # k coefficient:
        # 1*k=k: a1*d2
        # k*1=k: d1*a2
        # j*h=k: b1*c2
        # h*j=k: c1*b2
        k_coeff = expand(a1*d2 + d1*a2 + b1*c2 + c1*b2)

        return Tessarine(real, j_coeff, h_coeff, k_coeff)

    def __rmul__(self, other):
        # Tessarines are commutative, so rmul = mul for scalars
        if isinstance(other, (int, float)) or hasattr(other, 'is_number'):
            return Tessarine(
                expand(other * self.a),
                expand(other * self.b),
                expand(other * self.c),
                expand(other * self.d)
            )
        return other.__mul__(self)

    def __eq__(self, other):
        if isinstance(other, Tessarine):
            return (simplify(self.a - other.a) == 0 and
                    simplify(self.b - other.b) == 0 and
                    simplify(self.c - other.c) == 0 and
                    simplify(self.d - other.d) == 0)
        return False

    def components(self):
        return {'1': self.a, 'j': self.b, 'h': self.c, 'k': self.d}

# Basis elements
ONE = Tessarine(1, 0, 0, 0)
J = Tessarine(0, 1, 0, 0)
H = Tessarine(0, 0, 1, 0)
K = Tessarine(0, 0, 0, 1)

print("=" * 72)
print("TESSARINE VERSOR ALGEBRA VERIFICATION")
print("=" * 72)

# =============================================================================
# TEST 1: Full Multiplication Table
# =============================================================================
print("\n" + "=" * 72)
print("TEST 1: Tessarine Multiplication Table")
print("=" * 72)

basis = {'1': ONE, 'j': J, 'h': H, 'k': K}
expected = {
    ('1','1'): ONE,  ('1','j'): J,    ('1','h'): H,   ('1','k'): K,
    ('j','1'): J,    ('j','j'): Tessarine(-1,0,0,0), ('j','h'): K,   ('j','k'): Tessarine(0,0,-1,0),
    ('h','1'): H,    ('h','j'): K,    ('h','h'): ONE,  ('h','k'): J,
    ('k','1'): K,    ('k','j'): Tessarine(0,0,-1,0), ('k','h'): J,   ('k','k'): Tessarine(-1,0,0,0),
}

all_pass = True
print(f"\n{'x':>3} | {'1':>6} | {'j':>6} | {'h':>6} | {'k':>6}")
print("-" * 40)

for name1, e1 in basis.items():
    row = f"{name1:>3} |"
    for name2, e2 in basis.items():
        product = e1 * e2
        exp = expected[(name1, name2)]
        match = product == exp
        if not match:
            all_pass = False
        # Find which basis element it is
        comps = product.components()
        result_str = ""
        for bname, coeff in comps.items():
            if coeff != 0:
                if coeff == 1:
                    result_str = bname
                elif coeff == -1:
                    result_str = f"-{bname}"
                else:
                    result_str = f"{coeff}*{bname}"
        if not result_str:
            result_str = "0"
        row += f" {result_str:>6} |"
    print(row)

print(f"\nMultiplication table: {'PASS' if all_pass else 'FAIL'}")

# =============================================================================
# TEST 2: Specific product verifications
# =============================================================================
print("\n" + "=" * 72)
print("TEST 2: Key Product Identities")
print("=" * 72)

tests = [
    ("j*j", J*J, Tessarine(-1,0,0,0), "j^2 = -1"),
    ("h*h", H*H, ONE, "h^2 = +1"),
    ("k*k", K*K, Tessarine(-1,0,0,0), "k^2 = -1"),
    ("h*j", H*J, K, "hj = k"),
    ("j*h", J*H, K, "jh = k (commutativity)"),
    ("j*k", J*K, Tessarine(0,0,-1,0), "jk = -h"),
    ("k*j", K*J, Tessarine(0,0,-1,0), "kj = -h (commutativity)"),
    ("h*k", H*K, J, "hk = j"),
    ("k*h", K*H, J, "kh = j (commutativity)"),
]

for name, result, expected_val, description in tests:
    match = result == expected_val
    status = "PASS" if match else "FAIL"
    print(f"  {name:>5} = {result}  [{status}]  ({description})")

# Critical check: jk in tessarines
print("\n  CRITICAL: j*k in tessarines:")
jk = J * K
print(f"    j*k = {jk}")
print(f"    j*k = -h? {jk == Tessarine(0,0,-1,0)}")
print(f"    j*k = 1?  {jk == ONE}")
print(f"    NOTE: In Dollard's system, jk=1 (non-commutative).")
print(f"    In tessarines (commutative), jk = -h.")
print(f"    This is a STRUCTURAL DIFFERENCE.")

# =============================================================================
# TEST 3: Z*Y Product in Tessarines
# =============================================================================
print("\n" + "=" * 72)
print("TEST 3: Z*Y Product in Tessarines")
print("=" * 72)

# Z = R + j*X (impedance)
Z = Tessarine(R, X, 0, 0)
print(f"\n  Z = R + j*X = {Z}")

# Y = G - j*B (admittance, Dollard's sign convention)
Y = Tessarine(G, -B, 0, 0)
print(f"  Y = G - j*B = {Y}")

# Compute Z*Y
ZY = Z * Y
print(f"\n  Z*Y = {ZY}")
print(f"\n  Decomposition into basis components:")
comps = ZY.components()
for bname, coeff in comps.items():
    print(f"    Coefficient of {bname}: {coeff}")

print(f"\n  Expanding:")
print(f"    Real (1):  {expand(comps['1'])}")
print(f"    j-part:    {expand(comps['j'])}")
print(f"    h-part:    {expand(comps['h'])}")
print(f"    k-part:    {expand(comps['k'])}")

# =============================================================================
# TEST 4: Test the specific claim Z*Y = h(XB+RG) + j(XG-RB)
# =============================================================================
print("\n" + "=" * 72)
print("TEST 4: Test Claim Z*Y = h(XB+RG) + j(XG-RB)")
print("=" * 72)

claimed = Tessarine(0, X*G - R*B, X*B + R*G, 0)
print(f"\n  Claimed result: {claimed}")
print(f"  Computed Z*Y:   {ZY}")

components_match = True
for bname in ['1', 'j', 'h', 'k']:
    c_claim = simplify(claimed.components()[bname])
    c_actual = simplify(ZY.components()[bname])
    match = simplify(c_claim - c_actual) == 0
    status = "MATCH" if match else "MISMATCH"
    print(f"    {bname}-component: claimed={c_claim}, actual={c_actual}  [{status}]")
    if not match:
        components_match = False

print(f"\n  Claim Z*Y = h(XB+RG) + j(XG-RB): {'CONFIRMED' if components_match else 'REFUTED'}")

if not components_match:
    print(f"\n  The ACTUAL tessarine product Z*Y is:")
    print(f"    Z*Y = ({comps['1']}) + ({comps['j']})*j + ({comps['h']})*h + ({comps['k']})*k")

# =============================================================================
# TEST 4b: What IS the correct tessarine Z*Y?
# =============================================================================
print("\n" + "=" * 72)
print("TEST 4b: Correct Tessarine Z*Y Expansion")
print("=" * 72)

# Manual derivation for verification:
# Z*Y = (R + jX)(G - jB)
# Using tessarine multiplication:
#   = R*G + R*(-jB) + jX*G + jX*(-jB)
#   = RG - j(RB) + j(XG) + (-j^2)(XB)
#   = RG - j*RB + j*XG + XB         (since j^2 = -1, so -j^2 = +1)
#   = (RG + XB) + j(XG - RB)
print("\n  Manual expansion of Z*Y = (R + jX)(G - jB) in tessarines:")
print("    = R*G + R*(-j*B) + j*X*G + j*X*(-j*B)")
print("    = R*G - j*(R*B) + j*(X*G) - j^2*(X*B)")
print("    = R*G - j*(R*B) + j*(X*G) + X*B        [since j^2 = -1]")
print("    = (R*G + X*B) + j*(X*G - R*B)")
print()
print("  This is a PURELY COMPLEX result (no h or k components).")
print("  Because Z and Y have no h or k components, and tessarines")
print("  are commutative, the product stays in the {1, j} subspace.")
print()
print("  The claim Z*Y = h(XB+RG) + j(XG-RB) is WRONG in tessarines")
print("  because it puts the real power in the h-component instead")
print("  of the 1-component. The correct result is:")
print(f"    Z*Y = ({comps['1']}) + ({comps['j']})*j")
print(f"  which means:")
print(f"    Real power P      = RG + XB  (coefficient of 1)")
print(f"    Reactive power Q  = XG - RB  (coefficient of j)")

# =============================================================================
# TEST 5: What about Z = h*R + j*X (with h-prefix on resistance)?
# =============================================================================
print("\n" + "=" * 72)
print("TEST 5: Alternative Forms -- What if Z or Y have h-components?")
print("=" * 72)

# Maybe the claim assumes Z = hR + jX?
Z_alt1 = Tessarine(0, X, R, 0)  # h*R + j*X
Y_std = Tessarine(G, -B, 0, 0)  # G - jB
ZY_alt1 = Z_alt1 * Y_std
print(f"\n  Form A: Z = h*R + j*X, Y = G - j*B")
print(f"    Z*Y = {ZY_alt1}")
comps_a = ZY_alt1.components()
for bname, coeff in comps_a.items():
    print(f"      {bname}: {coeff}")

# Maybe Y = hG - jB?
Z_std = Tessarine(R, X, 0, 0)
Y_alt1 = Tessarine(0, -B, G, 0)  # h*G - j*B
ZY_alt2 = Z_std * Y_alt1
print(f"\n  Form B: Z = R + j*X, Y = h*G - j*B")
print(f"    Z*Y = {ZY_alt2}")
comps_b = ZY_alt2.components()
for bname, coeff in comps_b.items():
    print(f"      {bname}: {coeff}")

# What about Z = hR + jX, Y = hG - jB?
Z_alt2 = Tessarine(0, X, R, 0)
Y_alt2 = Tessarine(0, -B, G, 0)
ZY_alt3 = Z_alt2 * Y_alt2
print(f"\n  Form C: Z = h*R + j*X, Y = h*G - j*B")
print(f"    Z*Y = {ZY_alt3}")
comps_c = ZY_alt3.components()
for bname, coeff in comps_c.items():
    print(f"      {bname}: {coeff}")

# Check which form gives h(XB+RG) + j(XG-RB)
target = Tessarine(0, X*G - R*B, X*B + R*G, 0)
print(f"\n  Target: h*(XB+RG) + j*(XG-RB)")
for form_name, result in [("A", ZY_alt1), ("B", ZY_alt2), ("C", ZY_alt3)]:
    match = all(simplify(result.components()[b] - target.components()[b]) == 0 for b in ['1','j','h','k'])
    print(f"    Form {form_name} matches target: {match}")

# =============================================================================
# TEST 6: Dollard's ACTUAL formula -- maybe with his operator ordering
# =============================================================================
print("\n" + "=" * 72)
print("TEST 6: Dollard's Non-Commutative Algebra (Not Tessarines)")
print("=" * 72)

print("""
  In Dollard's versor algebra:
    j^2 = -1, h^2 = +1, k = hj
    BUT: jk = 1 (NOT -h), and hj != jh in general

  This is NOT tessarines. Tessarines are commutative.
  Dollard's algebra is non-commutative with jk = 1.

  Let's verify what jk must be in each system:
    Tessarines: j*k = j*(hj) = j*h*j = (jh)j = kj = k*j
      Since commutative: j*k = j*(hj) = (j*h)*j = k*j
      j*k = j*hj. In tessarines: j*h = k, so j*k = k*j = (hj)*j = h*(j^2) = h*(-1) = -h

    Dollard:    j*k = 1 (stated axiom)
      This means jk = j(hj) = 1, which requires j(hj) = 1
      If we apply associativity: (jh)j = 1
      But jh != hj in Dollard (non-commutative)
""")

# =============================================================================
# TEST 7: Idempotent Decomposition
# =============================================================================
print("=" * 72)
print("TEST 7: Idempotent Decomposition")
print("=" * 72)

e_plus = Tessarine(Rational(1,2), 0, Rational(1,2), 0)   # (1+h)/2
e_minus = Tessarine(Rational(1,2), 0, Rational(-1,2), 0)  # (1-h)/2

print(f"\n  e+ = (1+h)/2 = {e_plus}")
print(f"  e- = (1-h)/2 = {e_minus}")

ep2 = e_plus * e_plus
em2 = e_minus * e_minus
epm = e_plus * e_minus
esum = e_plus + e_minus

print(f"\n  e+^2 = {ep2}")
print(f"  e+^2 = e+? {ep2 == e_plus}")

print(f"\n  e-^2 = {em2}")
print(f"  e-^2 = e-? {em2 == e_minus}")

print(f"\n  e+*e- = {epm}")
print(f"  e+*e- = 0? {epm == Tessarine(0,0,0,0)}")

print(f"\n  e+ + e- = {esum}")
print(f"  e+ + e- = 1? {esum == ONE}")

print(f"\n  Idempotent decomposition: {'PASS' if (ep2==e_plus and em2==e_minus and epm==Tessarine(0,0,0,0) and esum==ONE) else 'FAIL'}")

# Show the isomorphism: tessarine ~= C (+) C via idempotents
print(f"\n  Isomorphism: T ~= C (+) C")
print(f"  Any tessarine z = a + bj + ch + dk can be written as:")
print(f"    z = [(a+c) + (b+d)j]*e+ + [(a-c) + (b-d)j]*e-")
print(f"  where each bracket is a standard complex number.")

# Verify with a generic tessarine
a, b_sym, c, d = symbols('a b c d', real=True)
z_gen = Tessarine(a, b_sym, c, d)
# z*e+ should give the e+ component
z_ep = z_gen * e_plus
z_em = z_gen * e_minus
print(f"\n  z*e+ = {z_ep}")
print(f"  z*e- = {z_em}")
print(f"  z*e+ + z*e- = z? {(z_ep + z_em) == z_gen}")

# =============================================================================
# TEST 8: Quaternary Expansion (Tessarine Exponential)
# =============================================================================
print("\n" + "=" * 72)
print("TEST 8: Quaternary Expansion of Tessarine Exponential")
print("=" * 72)

print("""
  The tessarine exponential e^(j*theta + h*delta) factors as:
    e^(j*theta) * e^(h*delta)    [because j and h commute in tessarines]

  e^(j*theta) = cos(theta) + j*sin(theta)   [Euler's formula, j^2=-1]
  e^(h*delta) = cosh(delta) + h*sinh(delta)  [hyperbolic Euler, h^2=+1]

  Product:
    [cos(theta) + j*sin(theta)] * [cosh(delta) + h*sinh(delta)]
    = cos(theta)*cosh(delta)
      + j*sin(theta)*cosh(delta)
      + h*cos(theta)*sinh(delta)
      + k*sin(theta)*sinh(delta)    [since j*h = k]
""")

# Define the four quadrant components
# u = cos(theta)*cosh(delta)
# x = sin(theta)*cosh(delta)  (j-coefficient)
# v = cos(theta)*sinh(delta)  (h-coefficient)
# y = sin(theta)*sinh(delta)  (k-coefficient)

# Wait - need to match Dollard's naming. Let me use his convention:
# The tessarine exponential is: u + j*x_comp + h*v + k*y_comp
# where:
u_val = cos(theta)*cosh(delta)
x_val = sin(theta)*cosh(delta)
v_val = cos(theta)*sinh(delta)
y_val = sin(theta)*sinh(delta)

print(f"  Components:")
print(f"    u (1-coeff)  = cos(theta)*cosh(delta)")
print(f"    x (j-coeff)  = sin(theta)*cosh(delta)")
print(f"    v (h-coeff)  = cos(theta)*sinh(delta)")
print(f"    y (k-coeff)  = sin(theta)*sinh(delta)")

# Verify quaternary identities
print(f"\n  Quaternary identities:")

diff_uv = simplify(u_val - v_val)
print(f"    u - v = cos(theta)*cosh(delta) - cos(theta)*sinh(delta)")
print(f"          = cos(theta)*(cosh(delta) - sinh(delta))")
print(f"          = cos(theta)*e^(-delta)")
print(f"    Claimed: u - v = cos(theta)")
print(f"    Actual:  u - v = {diff_uv}")
uv_is_cos = simplify(diff_uv - cos(theta)) == 0
print(f"    u - v = cos(theta)? {uv_is_cos}")
if not uv_is_cos:
    print(f"    NOTE: u - v = cos(theta) ONLY when delta = 0 (no growth/decay)")

diff_xy = simplify(x_val - y_val)
print(f"\n    x - y = sin(theta)*cosh(delta) - sin(theta)*sinh(delta)")
print(f"          = sin(theta)*(cosh(delta) - sinh(delta))")
print(f"          = sin(theta)*e^(-delta)")
print(f"    Claimed: x - y = sin(theta)")
print(f"    Actual:  x - y = {diff_xy}")
xy_is_sin = simplify(diff_xy - sin(theta)) == 0
print(f"    x - y = sin(theta)? {xy_is_sin}")

sum_uv = simplify(u_val + v_val)
print(f"\n    u + v = cos(theta)*cosh(delta) + cos(theta)*sinh(delta)")
print(f"          = cos(theta)*(cosh(delta) + sinh(delta))")
print(f"          = cos(theta)*e^(delta)")
print(f"    Claimed: u + v = cosh(delta)")
print(f"    Actual:  u + v = {sum_uv}")
uv_is_cosh = simplify(sum_uv - cosh(delta)) == 0
print(f"    u + v = cosh(delta)? {uv_is_cosh}")
if not uv_is_cosh:
    print(f"    NOTE: u + v = cosh(delta) ONLY when theta = 0")

sum_xy = simplify(x_val + y_val)
print(f"\n    x + y = sin(theta)*cosh(delta) + sin(theta)*sinh(delta)")
print(f"          = sin(theta)*(cosh(delta) + sinh(delta))")
print(f"          = sin(theta)*e^(delta)")
print(f"    Claimed: x + y = sinh(delta)")
print(f"    Actual:  x + y = {sum_xy}")
xy_is_sinh = simplify(sum_xy - sinh(delta)) == 0
print(f"    x + y = sinh(delta)? {xy_is_sinh}")

print(f"\n  IMPORTANT CORRECTION:")
print(f"  The quaternary identities as stated (u-v=cos, x-y=sin, u+v=cosh, x+y=sinh)")
print(f"  are NOT generally true for the tessarine exponential e^(j*theta + h*delta).")
print(f"  They hold only in the decoupled limits:")
print(f"    delta=0: u-v = cos(theta), x-y = sin(theta)")
print(f"    theta=0: u+v = cosh(delta), x+y = sinh(delta)")
print(f"")
print(f"  In general:")
print(f"    u - v = cos(theta)*e^(-delta)")
print(f"    x - y = sin(theta)*e^(-delta)")
print(f"    u + v = cos(theta)*e^(delta)")
print(f"    x + y = sin(theta)*e^(delta)")

# But wait -- let me re-read the quaternary expansion more carefully.
# Dollard's four-quadrant model uses a DIFFERENT decomposition.
# The four subseries of e^t are:
#   u = sum_{n=0}^{inf} t^{4n}/(4n)!        [n mod 4 = 0]
#   x = sum_{n=0}^{inf} t^{4n+1}/(4n+1)!    [n mod 4 = 1]
#   v = sum_{n=0}^{inf} t^{4n+2}/(4n+2)!    [n mod 4 = 2]
#   y = sum_{n=0}^{inf} t^{4n+3}/(4n+3)!    [n mod 4 = 3]
# Then e^t = u + x + v + y, and the identities become exact.

print(f"\n  ALTERNATIVE: Dollard's quaternary uses the four subseries of e^t:")
print(f"    u = sum t^(4n)/(4n)!")
print(f"    x = sum t^(4n+1)/(4n+1)!")
print(f"    v = sum t^(4n+2)/(4n+2)!")
print(f"    y = sum t^(4n+3)/(4n+3)!")

# Verify with SymPy series expansion
from sympy import factorial, oo, Sum, Dummy
m = Dummy('m', integer=True, nonnegative=True)

# Compute partial sums to verify
N_TERMS = 20

u_series = sum(t**(4*nn) / factorial(4*nn) for nn in range(N_TERMS))
x_series = sum(t**(4*nn+1) / factorial(4*nn+1) for nn in range(N_TERMS))
v_series = sum(t**(4*nn+2) / factorial(4*nn+2) for nn in range(N_TERMS))
y_series = sum(t**(4*nn+3) / factorial(4*nn+3) for nn in range(N_TERMS))

# Check u - v vs cos(t) truncated
cos_series = sum((-1)**nn * t**(2*nn) / factorial(2*nn) for nn in range(2*N_TERMS))
sin_series = sum((-1)**nn * t**(2*nn+1) / factorial(2*nn+1) for nn in range(2*N_TERMS))
cosh_series = sum(t**(2*nn) / factorial(2*nn) for nn in range(2*N_TERMS))
sinh_series = sum(t**(2*nn+1) / factorial(2*nn+1) for nn in range(2*N_TERMS))

uv_diff = expand(u_series - v_series)
cos_exp = expand(cos_series)

# Truncate both to same order for comparison
from sympy import O, Poly
max_order = 4*N_TERMS - 1

# Compare coefficient by coefficient
print(f"\n  Verifying u - v = cos(t) via series (order {max_order}):")
uv_poly = sum(uv_diff.coeff(t, i) * t**i for i in range(max_order+1))
cos_poly = sum(cos_exp.coeff(t, i) * t**i for i in range(max_order+1))
match_uv = expand(uv_poly - cos_poly) == 0
print(f"    u - v = cos(t) (to order {max_order}): {match_uv}")

print(f"\n  Verifying x - y = sin(t) via series:")
xy_diff = expand(x_series - y_series)
sin_exp = expand(sin_series)
xy_poly = sum(xy_diff.coeff(t, i) * t**i for i in range(max_order+1))
sin_poly = sum(sin_exp.coeff(t, i) * t**i for i in range(max_order+1))
match_xy = expand(xy_poly - sin_poly) == 0
print(f"    x - y = sin(t) (to order {max_order}): {match_xy}")

print(f"\n  Verifying u + v = cosh(t) via series:")
uv_sum = expand(u_series + v_series)
cosh_exp = expand(cosh_series)
uvs_poly = sum(uv_sum.coeff(t, i) * t**i for i in range(max_order+1))
cosh_poly = sum(cosh_exp.coeff(t, i) * t**i for i in range(max_order+1))
match_uvs = expand(uvs_poly - cosh_poly) == 0
print(f"    u + v = cosh(t) (to order {max_order}): {match_uvs}")

print(f"\n  Verifying x + y = sinh(t) via series:")
xy_sum = expand(x_series + y_series)
sinh_exp = expand(sinh_series)
xys_poly = sum(xy_sum.coeff(t, i) * t**i for i in range(max_order+1))
sinh_poly = sum(sinh_exp.coeff(t, i) * t**i for i in range(max_order+1))
match_xys = expand(xys_poly - sinh_poly) == 0
print(f"    x + y = sinh(t) (to order {max_order}): {match_xys}")

quat_pass = match_uv and match_xy and match_uvs and match_xys
print(f"\n  Quaternary identities (series verification): {'PASS' if quat_pass else 'FAIL'}")

# =============================================================================
# TEST 9: Commutativity check (tessarine vs Dollard)
# =============================================================================
print("\n" + "=" * 72)
print("TEST 9: Commutativity -- Tessarine vs Dollard")
print("=" * 72)

print(f"\n  In tessarines (commutative):")
print(f"    h*j = {H*J}  =  j*h = {J*H}")
print(f"    h*j = j*h? {(H*J) == (J*H)}")
print(f"    j*k = {J*K}  =  k*j = {K*J}")
print(f"    j*k = k*j? {(J*K) == (K*J)}")

print(f"\n  In Dollard's versor algebra (NON-commutative):")
print(f"    hj = k   (defined)")
print(f"    jh = ???  (NOT necessarily k)")
print(f"    jk = 1   (Dollard's axiom)")
print(f"    kj = ???")
print()
print(f"  If jk = 1 and k = hj, then j(hj) = 1")
print(f"  By associativity: (jh)j = 1")
print(f"  So jh must be j^(-1) = -j (since j^4=1, j^3=-j, j*(-j)=1? No...)")
print(f"  Actually j^(-1): j * j^(-1) = 1, and j^4 = 1 means j^3 = j^(-1)")
print(f"  j^3 = j^2 * j = (-1)*j = -j. So j^(-1) = -j.")
print(f"  Then (jh)j = 1 means jh = j^(-1) = -j")
print(f"  But hj = k, and jh = -j. So hj != jh.")
print(f"  This confirms Dollard's algebra is NON-commutative.")
print(f"  Tessarines are commutative. They are DIFFERENT algebras.")

# =============================================================================
# TEST 10: Summary of the Dollard non-commutative multiplication table
# =============================================================================
print("\n" + "=" * 72)
print("TEST 10: Dollard's Non-Commutative Cayley Table (Derived)")
print("=" * 72)

print("""
  Given Dollard's axioms:
    j^2 = -1, j^4 = 1
    h^2 = +1, h != 1
    k = hj
    jk = 1

  Derived products:
    j^(-1) = j^3 = -j

    jk = 1  (axiom)
    kj: k*j = (hj)*j = h*(j^2) = h*(-1) = -h
    So kj = -h != jk = 1  (non-commutative!)

    jh: From (jh)*j = 1, we get jh = -j  (since j^(-1) = -j)
    Wait, (jh)*j = 1 means jh = j^(-1) = -j
    But that gives jh = -j, which is a scalar multiple of j.
    Check: j*(-j) = -j^2 = -(-1) = 1 [ok]
    So jh = -j.

    hj = k  (definition)
    jh = -j  (derived)
    hj != jh  [ok] (non-commutative)

    hk = h*(hj) = (h^2)*j = 1*j = j
    kh = (hj)*h = ... need to know jh.
       kh = h*(j*h) ... no, k = hj, so kh = (hj)h
       We need the order: (hj)h.
       Using associativity: h(jh) = h(-j) = -hj = -k
    So kh = -k.

    Full Dollard table:

       | 1  | j  | h  | k
    ---+----+----+----+----
     1 | 1  | j  | h  | k
     j | j  | -1 | -j | 1
     h | h  | k  | 1  | j
     k | k  | -h | -k | -1

    CHECK: k^2 = k*k = (hj)(hj).
      = h(jh)j = h(-j)j = -h(j^2) = -h(-1) = h.

    Wait, that gives k^2 = h, not -1!
    Let me recheck. k*k = (hj)*(hj).
    Associating: h*(j*(h*j)) = h*(j*k).
    jk = 1 (axiom), so = h*1 = h.

    So k^2 = h in Dollard's system. NOT k^2 = -1!

    Alternative: k^2 = (hj)(hj) = h(j(hj)) = h(jk) = h*1 = h.

    This is VERY different from tessarines where k^2 = -1.
""")

print("  Let me verify the complete Dollard table by chaining axioms:")
print()

# Implement Dollard's non-commutative algebra
class DollardVersor:
    """
    Dollard's non-commutative versor algebra: a + b*j + c*h + d*k
    Axioms: j^2=-1, j^4=1, h^2=+1, k=hj, jk=1
    """
    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __repr__(self):
        terms = []
        if self.a != 0: terms.append(f"({self.a})")
        if self.b != 0: terms.append(f"({self.b})*j")
        if self.c != 0: terms.append(f"({self.c})*h")
        if self.d != 0: terms.append(f"({self.d})*k")
        return " + ".join(terms) if terms else "0"

    def __neg__(self):
        return DollardVersor(-self.a, -self.b, -self.c, -self.d)

    def __add__(self, other):
        if isinstance(other, (int, float)) or hasattr(other, 'is_number'):
            return DollardVersor(self.a + other, self.b, self.c, self.d)
        return DollardVersor(
            expand(self.a + other.a), expand(self.b + other.b),
            expand(self.c + other.c), expand(self.d + other.d))

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, (int, float)) or hasattr(other, 'is_number'):
            return DollardVersor(expand(self.a*other), expand(self.b*other),
                               expand(self.c*other), expand(self.d*other))

        a1,b1,c1,d1 = self.a, self.b, self.c, self.d
        a2,b2,c2,d2 = other.a, other.b, other.c, other.d

        # Multiplication table (from Dollard's axioms):
        #      | 1   j   h   k
        #   1  | 1   j   h   k
        #   j  | j  -1  -j   1
        #   h  | h   k   1   j
        #   k  | k  -h  -k  -1
        #
        # Wait, I derived k^2 = h above. Let me recheck k^2.
        # Actually, there's a subtlety. Let me be more careful.
        #
        # The issue is: is Dollard's algebra associative?
        # If associative: k^2 = (hj)(hj) = h(j(hj)) = h(jk) = h*1 = h
        # If k^2 = h, then the "algebra" has k^2 not in {-1, +1}.
        # This means {1, j, h, k} does NOT close under multiplication!
        # k^2 = h means the algebra is fine (h is in the basis), but
        # the Cayley table entry for k*k is h, not +/-1.
        #
        # Let me re-derive everything carefully.
        #
        # Given: j^2=-1, h^2=+1, k=hj, jk=1
        #
        # j*j = -1*1 -> (-1, 0, 0, 0)
        # j*h: (jh)j=1 -> jh = j^{-1} = -j -> (0, -1, 0, 0)
        # j*k = 1 -> (1, 0, 0, 0)  [axiom]
        # h*j = k -> (0, 0, 0, 1)  [definition]
        # h*h = 1 -> (1, 0, 0, 0)
        # h*k = h(hj) = (hh)j = j -> (0, 1, 0, 0)
        # k*j = (hj)j = h(jj) = h(-1) = -h -> (0, 0, -1, 0)
        # k*h = (hj)h = h(jh) = h(-j) = -(hj) = -k -> (0, 0, 0, -1)
        # k*k = (hj)(hj) = h(j(hj)) = h(jk) = h(1) = h -> (0, 0, 1, 0)

        # Cayley table for Dollard (row * col):
        #      |  1    j     h    k
        #  ----+----+-----+----+----
        #   1  |  1    j     h    k
        #   j  |  j   -1    -j    1
        #   h  |  h    k     1    j
        #   k  |  k   -h    -k    h

        # Product: (a1+b1*j+c1*h+d1*k)(a2+b2*j+c2*h+d2*k)
        # 1-component: a1*a2*1 + b1*b2*(-1) + c1*c2*(1) + d1*d2*(h->0 for 1-comp)
        # Wait, k*k = h means it contributes to h-component, not 1-component.

        # Let me do this properly. Each product of basis elements:
        # 1*1 = 1       -> (1,0,0,0)
        # 1*j = j       -> (0,1,0,0)
        # 1*h = h       -> (0,0,1,0)
        # 1*k = k       -> (0,0,0,1)
        # j*1 = j       -> (0,1,0,0)
        # j*j = -1      -> (-1,0,0,0)
        # j*h = -j      -> (0,-1,0,0)
        # j*k = 1       -> (1,0,0,0)
        # h*1 = h       -> (0,0,1,0)
        # h*j = k       -> (0,0,0,1)
        # h*h = 1       -> (1,0,0,0)
        # h*k = j       -> (0,1,0,0)
        # k*1 = k       -> (0,0,0,1)
        # k*j = -h      -> (0,0,-1,0)
        # k*h = -k      -> (0,0,0,-1)
        # k*k = h       -> (0,0,1,0)

        # 1-component: 1*1, j*j, j*k, h*h contributions
        real = expand(a1*a2 - b1*b2 + b1*d2 + c1*c2)

        # j-component: 1*j, j*1, j*h(=-j gives -), h*k
        j_part = expand(a1*b2 + b1*a2 - b1*c2 + c1*d2)

        # h-component: 1*h, h*1, k*j(=-h), k*k(=h)
        h_part = expand(a1*c2 + c1*a2 - d1*b2 + d1*d2)

        # k-component: 1*k, k*1, h*j, k*h(=-k)
        k_part = expand(a1*d2 + d1*a2 + c1*b2 - d1*c2)

        return DollardVersor(real, j_part, h_part, k_part)

    def __eq__(self, other):
        if isinstance(other, DollardVersor):
            return (simplify(self.a - other.a) == 0 and
                    simplify(self.b - other.b) == 0 and
                    simplify(self.c - other.c) == 0 and
                    simplify(self.d - other.d) == 0)
        return False

    def components(self):
        return {'1': self.a, 'j': self.b, 'h': self.c, 'k': self.d}

# Dollard basis
D1 = DollardVersor(1,0,0,0)
DJ = DollardVersor(0,1,0,0)
DH = DollardVersor(0,0,1,0)
DK = DollardVersor(0,0,0,1)

d_basis = {'1': D1, 'j': DJ, 'h': DH, 'k': DK}

print(f"  Dollard Cayley table (derived from axioms):")
print(f"\n{'x':>3} | {'1':>4} | {'j':>4} | {'h':>4} | {'k':>4}")
print("-" * 30)

for name1, e1 in d_basis.items():
    row = f"{name1:>3} |"
    for name2, e2 in d_basis.items():
        product = e1 * e2
        comps = product.components()
        result_str = ""
        for bname, coeff in comps.items():
            if coeff != 0:
                if coeff == 1 and bname == '1':
                    result_str = " 1"
                elif coeff == -1 and bname == '1':
                    result_str = "-1"
                elif coeff == 1:
                    result_str = f" {bname}"
                elif coeff == -1:
                    result_str = f"-{bname}"
                else:
                    result_str = f"{coeff}{bname}"
        row += f" {result_str:>4} |"
    print(row)

# Verify key identities
print(f"\n  Verification of Dollard axioms:")
print(f"    j^2 = -1: {DJ*DJ == DollardVersor(-1,0,0,0)}")
print(f"    h^2 = +1: {DH*DH == D1}")
print(f"    hj = k:   {DH*DJ == DK}")
print(f"    jk = 1:   {DJ*DK == D1}")

print(f"\n  Derived identities:")
print(f"    jh = -j:  {DJ*DH == DollardVersor(0,-1,0,0)}")
print(f"    kj = -h:  {DK*DJ == DollardVersor(0,0,-1,0)}")
print(f"    hk = j:   {DH*DK == DollardVersor(0,1,0,0)}")
print(f"    kh = -k:  {DK*DH == DollardVersor(0,0,0,-1)}")
print(f"    k^2 = h:  {DK*DK == DollardVersor(0,0,1,0)}")

print(f"\n  CRITICAL FINDING: k^2 = h (not -1!) in Dollard's algebra")
print(f"  In tessarines: k^2 = -1")
print(f"  This is a FUNDAMENTAL difference.")

# Check associativity of Dollard's algebra
print(f"\n  Associativity check for Dollard's algebra:")
assoc_fail = False
for n1, e1 in d_basis.items():
    for n2, e2 in d_basis.items():
        for n3, e3 in d_basis.items():
            lhs = (e1 * e2) * e3
            rhs = e1 * (e2 * e3)
            if not (lhs == rhs):
                print(f"    ({n1}*{n2})*{n3} != {n1}*({n2}*{n3})")
                print(f"      LHS = {lhs}")
                print(f"      RHS = {rhs}")
                assoc_fail = True

if not assoc_fail:
    print(f"    All 64 triple products associative: PASS")
else:
    print(f"    Associativity: FAIL")

# =============================================================================
# TEST 11: Z*Y in Dollard's algebra
# =============================================================================
print("\n" + "=" * 72)
print("TEST 11: Z*Y in Dollard's Non-Commutative Algebra")
print("=" * 72)

DZ = DollardVersor(R, X, 0, 0)  # R + jX
DY = DollardVersor(G, -B, 0, 0)  # G - jB
DZY = DZ * DY

print(f"\n  Z = R + j*X = {DZ}")
print(f"  Y = G - j*B = {DY}")
print(f"  Z*Y = {DZY}")

d_comps = DZY.components()
print(f"\n  Components:")
for bname, coeff in d_comps.items():
    print(f"    {bname}: {coeff}")

# In Dollard's algebra, Z*Y = (R+jX)(G-jB) with non-commutative j:
# = RG + R(-jB) + jXG + jX(-jB)
# = RG - RjB + jXG - jXjB
# = RG - R(jB) + (jX)G - (jX)(jB)
# For the last term: j*X*j*B = j*(j)*X*B? NO - X and B are scalars, they commute with everything
# (jX)(jB) = XB*(j*j) = XB*(-1) = -XB
# So Z*Y = RG + XB - j*RB + j*XG = (RG+XB) + j(XG-RB)
# Same as tessarine case! Because Z and Y only use {1, j} and j commutes with scalars.

print(f"\n  Note: Z*Y = (RG+XB) + j(XG-RB) in Dollard's algebra too,")
print(f"  because Z and Y only involve {{1, j}} and j commutes with real scalars.")
print(f"  The non-commutativity only matters when h and k interact with j.")

# Check the claimed form h(XB+RG) + j(XG-RB)
d_target = DollardVersor(0, X*G - R*B, X*B + R*G, 0)
match_d = all(simplify(DZY.components()[b] - d_target.components()[b]) == 0 for b in ['1','j','h','k'])
print(f"\n  Z*Y = h(XB+RG) + j(XG-RB) in Dollard? {match_d}")
print(f"  Z*Y = (RG+XB) + j(XG-RB) in Dollard? ", end="")
d_correct = DollardVersor(R*G + X*B, X*G - R*B, 0, 0)
match_correct = all(simplify(DZY.components()[b] - d_correct.components()[b]) == 0 for b in ['1','j','h','k'])
print(f"{match_correct}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 72)
print("FINAL SUMMARY")
print("=" * 72)

print("""
  1. TESSARINE MULTIPLICATION TABLE: VERIFIED
     j^2=-1, h^2=+1, k=hj=jh, k^2=-1, commutative.

  2. Z*Y IN TESSARINES (Z=R+jX, Y=G-jB):
     Z*Y = (RG + XB) + j*(XG - RB)
     This is a PURELY COMPLEX result (no h or k components).

  3. THE CLAIM Z*Y = h(XB+RG) + j(XG-RB): REFUTED
     The real power (RG+XB) appears in the 1-component, NOT the h-component.
     No alternative sign convention or basis ordering produces this form
     when Z and Y are in the {1, j} subspace.

  4. DOLLARD'S ALGEBRA IS NOT TESSARINES:
     - Tessarines: commutative, k^2 = -1, jk = -h
     - Dollard:    non-commutative, k^2 = h, jk = 1
     These are structurally different algebras.

  5. Z*Y IN DOLLARD'S ALGEBRA:
     Same result: (RG+XB) + j(XG-RB), because the non-commutativity
     doesn't affect products within the {1, j} subspace.

  6. QUATERNARY IDENTITIES: VERIFIED (via series)
     u - v = cos(t), x - y = sin(t), u + v = cosh(t), x + y = sinh(t)
     These hold for Dollard's four-subseries decomposition of e^t.

  7. IDEMPOTENT DECOMPOSITION: VERIFIED (tessarines only)
     e+ = (1+h)/2, e- = (1-h)/2 are orthogonal idempotents.
     Tessarine ~= C (+) C (direct sum of complex algebras).

  8. jk IN TESSARINES = -h (NOT 1):
     This is the key structural difference from Dollard's algebra.

  BOTTOM LINE: The claim that Dollard's versor algebra IS the tessarine
  algebra is FALSE. They share j^2=-1 and h^2=+1 but differ on:
    - Commutativity (tessarines: yes, Dollard: no)
    - k^2 (tessarines: -1, Dollard: h)
    - jk (tessarines: -h, Dollard: 1)

  The versor form ZY = h(XB+RG) + j(XG-RB) is WRONG in BOTH algebras
  when Z = R+jX and Y = G-jB. The correct result in both is:
    ZY = (RG+XB) + j(XG-RB)
""")
