"""
Build the Dollard Bookkeeping Discovery presentation.
Embeds all 5 figures as base64 and outputs a self-contained HTML file.
"""
import json
import base64

# Load pre-encoded images
with open('src/experiments/results/_img_b64.json', 'r') as f:
    imgs = json.load(f)

# If images not pre-encoded, encode them now
if not imgs:
    files = {
        'dollard_key_insight': 'src/experiments/results/dollard_key_insight.png',
        'tesla_coil_energy_map': 'src/experiments/results/tesla_coil_energy_map.png',
        'dollard_income_expenses': 'src/experiments/results/dollard_income_expenses.png',
        'dollard_vs_standard': 'src/experiments/results/dollard_vs_standard.png',
        'tesla_coil_four_quadrant': 'src/experiments/results/tesla_coil_four_quadrant.png',
    }
    for key, path in files.items():
        with open(path, 'rb') as img:
            imgs[key] = base64.b64encode(img.read()).decode('ascii')

CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Georgia', serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.7; }
  .slide { min-height: 100vh; padding: 60px 80px; display: flex; flex-direction: column; justify-content: center; border-bottom: 2px solid #222; }
  .slide:nth-child(odd) { background: #0a0a0a; }
  .slide:nth-child(even) { background: #0d0d12; }
  h1 { font-size: 3em; color: #f0c040; margin-bottom: 20px; letter-spacing: -1px; }
  h2 { font-size: 2em; color: #70b0ff; margin-bottom: 15px; }
  h3 { font-size: 1.4em; color: #a0d0a0; margin: 20px 0 10px 0; }
  p { font-size: 1.15em; margin-bottom: 15px; max-width: 900px; }
  .big { font-size: 1.5em; color: #f0c040; font-weight: bold; }
  .highlight { background: #2a2a00; border-left: 4px solid #f0c040; padding: 15px 20px; margin: 20px 0; }
  .math-block { background: #111; border: 1px solid #333; border-radius: 8px; padding: 20px 25px; margin: 20px 0; font-family: 'Courier New', monospace; font-size: 1.1em; color: #a0ffa0; overflow-x: auto; max-width: 900px; }
  .truth-box { background: #0a1a0a; border: 2px solid #2a5a2a; border-radius: 8px; padding: 15px 20px; margin: 15px 0; max-width: 900px; }
  .truth-box h4 { color: #4a9a4a; font-size: 1em; margin-bottom: 8px; }
  .truth-box code { color: #80c080; font-size: 0.95em; }
  .figure { margin: 30px 0; text-align: center; }
  .figure img { max-width: 100%; border: 1px solid #333; border-radius: 4px; }
  .figure .caption { font-style: italic; color: #999; margin-top: 10px; font-size: 0.95em; }
  table { border-collapse: collapse; margin: 20px 0; }
  th, td { border: 1px solid #444; padding: 10px 15px; text-align: left; }
  th { background: #1a1a2a; color: #70b0ff; }
  td { background: #111; }
  .num { color: #f0c040; font-weight: bold; font-size: 1.3em; }
  .dead { color: #ff5050; }
  .alive { color: #50ff50; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
  @media (max-width: 900px) { .two-col { grid-template-columns: 1fr; } .slide { padding: 30px 20px; } h1 { font-size: 2em; } }
  a { color: #70b0ff; }
  code { font-family: 'Courier New', monospace; color: #a0d0a0; }
  nav { position: fixed; top: 0; right: 0; background: #111; border-bottom-left-radius: 8px; padding: 10px 20px; z-index: 100; font-size: 0.85em; }
  nav a { color: #666; text-decoration: none; margin: 0 8px; }
  nav a:hover { color: #f0c040; }
"""

def img_tag(key, alt):
    return f'<img src="data:image/png;base64,{imgs[key]}" alt="{alt}">'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Gross/Net Discovery: What Dollard's Notation Reveals</title>
<style>{CSS}</style>
</head>
<body>

<nav>
  <a href="#title">Top</a>
  <a href="#question">Question</a>
  <a href="#method">Method</a>
  <a href="#math">Math</a>
  <a href="#fig1">Fig 1</a>
  <a href="#fig2">Fig 2</a>
  <a href="#fig3">Fig 3</a>
  <a href="#numbers">Numbers</a>
  <a href="#connection">N-Phase</a>
  <a href="#truth">Truth</a>
</nav>

<!-- SLIDE 1: TITLE -->
<div class="slide" id="title">
  <h1>The Gross/Net Discovery</h1>
  <h2>What Dollard's Notation Reveals That Standard Notation Hides</h2>
  <p style="color: #999; font-size: 1.3em; margin-top: 30px;">
    Ian Michael Arnoldy<br>
    Dollard Formal Verification Project<br>
    2026-03-17
  </p>
  <p style="margin-top: 40px; color: #666;">
    88 Lean 4 proof files &middot; ~2,900 verified declarations &middot; zero sorry gaps<br>
    5 computation scripts &middot; 5 generated figures &middot; 21 research documents
  </p>
</div>

<!-- SLIDE 2: THE QUESTION -->
<div class="slide" id="question">
  <h1>The Question</h1>
  <div class="highlight">
    <p class="big">"What does Dollard's mathematics imply if we follow it strictly on its own terms, WITHOUT mapping it into the standard model?"</p>
  </div>
  <p>We had already proved his algebra collapses to Z&#8324; (the cyclic group {{1, i, -1, -i}}). The Lean proof is in <code>algebraic_necessity.lean</code>. That question is settled.</p>
  <p>The new question was: <strong>even though the algebra is standard, does his NOTATION reveal structure that standard notation compresses away?</strong></p>
  <h3>What We Did</h3>
  <p>Launched a 5-round Research Council (Heptapod B + Polymathic Researcher + Dollard Theorist), followed by computational verification. Three agents proposed a tessarine hypothesis. A fourth agent killed it with algebra. Then we looked at what <em>survived</em>.</p>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      Algebra proof: src/lean_proofs/foundations/algebraic_necessity.lean<br>
      Tessarine refutation: research/tessarine-discovery/04-algebraic-verification-REFUTED.md<br>
      Council verdict: research/council/dollard-pure-construction/VERDICT.md<br>
      Verification script: src/experiments/tessarine_versor_verification.py
    </code>
  </div>
</div>

<!-- SLIDE 3: THE QUATERNARY DECOMPOSITION -->
<div class="slide" id="method">
  <h1>The Quaternary Decomposition</h1>
  <p>Dollard decomposes the exponential e<sup>t</sup> into <strong>four subseries</strong> indexed by power mod 4:</p>

  <div class="math-block">
u = &Sigma; t<sup>4n</sup> / (4n)! &emsp;&emsp;&emsp; terms where power &equiv; 0 mod 4<br>
x = &Sigma; t<sup>4n+1</sup> / (4n+1)! &emsp; terms where power &equiv; 1 mod 4<br>
v = &Sigma; t<sup>4n+2</sup> / (4n+2)! &emsp; terms where power &equiv; 2 mod 4<br>
y = &Sigma; t<sup>4n+3</sup> / (4n+3)! &emsp; terms where power &equiv; 3 mod 4
  </div>

  <p>These satisfy <strong>exact identities</strong> (verified to 10<sup>-50</sup>):</p>

  <div class="two-col">
    <div class="math-block">
<span style="color:#70b0ff">NET (circular):</span><br>
u - v = cos(t)<br>
x - y = sin(t)
    </div>
    <div class="math-block">
<span style="color:#ff7070">GROSS (hyperbolic):</span><br>
u + v = cosh(t)<br>
x + y = sinh(t)
    </div>
  </div>

  <p style="margin-top:20px;">And: &ensp;<code>u + x + v + y = e<sup>t</sup></code>&ensp; (the full exponential).</p>
  <p>Standard notation shows you <strong>cos(t)</strong> &mdash; the NET. Dollard's decomposition shows you that cos(t) is the <em>difference</em> of two terms (u and v) that can be <strong>individually enormous</strong>.</p>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      Implementation: src/experiments/dollard_vs_standard_comparison.py:28-60<br>
      Also: src/experiments/dollard_key_plots.py:12-24<br>
      Also: src/experiments/tesla_coil_four_quadrant.py:32-47<br>
      Lean (polyphase): src/lean_proofs/polyphase/polyphase_formula.lean<br>
      Verification: research/council/dollard-pure-construction/04-computation.md
    </code>
  </div>
</div>

<!-- SLIDE 4: THE MATH IN CODE -->
<div class="slide" id="math">
  <h1>The Implementation</h1>
  <p>The core computation. Three scripts implement this independently.</p>

  <div class="math-block" style="font-size: 0.95em;">
<span style="color:#f0c040">def</span> quaternary_subseries(t, N_terms=40):<br>
&emsp;&emsp;<span style="color:#666"># Dollard's four subseries of e^t</span><br>
&emsp;&emsp;u = zeros_like(t)<br>
&emsp;&emsp;x = zeros_like(t)<br>
&emsp;&emsp;v = zeros_like(t)<br>
&emsp;&emsp;y = zeros_like(t)<br>
&emsp;&emsp;<span style="color:#f0c040">for</span> n <span style="color:#f0c040">in</span> range(N_terms):<br>
&emsp;&emsp;&emsp;&emsp;k0, k1, k2, k3 = 4*n, 4*n+1, 4*n+2, 4*n+3<br>
&emsp;&emsp;&emsp;&emsp;u += t**k0 / factorial(k0) &emsp;<span style="color:#666"># power &equiv; 0 mod 4</span><br>
&emsp;&emsp;&emsp;&emsp;x += t**k1 / factorial(k1) &emsp;<span style="color:#666"># power &equiv; 1 mod 4</span><br>
&emsp;&emsp;&emsp;&emsp;v += t**k2 / factorial(k2) &emsp;<span style="color:#666"># power &equiv; 2 mod 4</span><br>
&emsp;&emsp;&emsp;&emsp;y += t**k3 / factorial(k3) &emsp;<span style="color:#666"># power &equiv; 3 mod 4</span><br>
&emsp;&emsp;<span style="color:#f0c040">return</span> u, x, v, y
  </div>

  <h3>The Gross/Net Ratio</h3>
  <div class="math-block">
<span style="color:#ff7070">gross</span> = u + v = cosh(&beta;x) &emsp;&emsp;<span style="color:#666"># total energy cycling through the system</span><br>
<span style="color:#70b0ff">net</span> &ensp; = |u - v| = |cos(&beta;x)| &emsp;<span style="color:#666"># what standard EE measures</span><br>
<br>
<span style="color:#f0c040">ratio</span> = gross / net = cosh(&beta;x) / |cos(&beta;x)|
  </div>

  <p>When &beta;x &rarr; &pi;/2 (quarter-wave resonance): cos &rarr; 0, cosh &rarr; 2.51. The ratio &rarr; infinity.</p>
  <p><strong>Standard EE sees net approaching 0 and says "nothing here." Dollard's bookkeeping sees gross = 2.51 and says "enormous energy is circulating."</strong></p>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      Gross/net computation: src/experiments/tesla_coil_four_quadrant.py:100-120<br>
      Ratio sweep: src/experiments/dollard_key_plots.py:76-96<br>
      Tesla coil model: src/experiments/tesla_coil_four_quadrant.py:54-95 (TeslaCoilSecondary class)
    </code>
  </div>
</div>

<!-- SLIDE 5: FIGURE 1 -->
<div class="slide" id="fig1">
  <h1>Figure 1: The Core Insight</h1>
  <div class="figure">
    {img_tag('dollard_key_insight', 'Dollard Key Insight')}
    <div class="caption">Three panels showing what Dollard's notation reveals that standard notation hides.</div>
  </div>
  <div class="two-col" style="margin-top: 20px;">
    <div>
      <h3>Panel A: Gross vs Net</h3>
      <p>At t=5: gross (cosh) = <span class="num">74.2</span>, net (cos) = <span class="num">0.28</span>. Ratio = <span class="num">260x</span>. Standard notation shows you the flat black line. Dollard shows you the red explosion.</p>
    </div>
    <div>
      <h3>Panel C: The h Distinction</h3>
      <p>Same symbol "h", but: h-as-number gives -e = -2.72 (negation). h-as-operator gives 1/e = 0.37 (reciprocation). <strong>Different physics, same notation.</strong></p>
    </div>
  </div>
  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>Generated by: src/experiments/dollard_key_plots.py:30-138</code>
  </div>
</div>

<!-- SLIDE 6: FIGURE 2 -->
<div class="slide" id="fig2">
  <h1>Figure 2: Tesla Coil Four-Quadrant Energy Map</h1>
  <div class="figure">
    {img_tag('tesla_coil_energy_map', 'Tesla Coil Energy Map')}
    <div class="caption">Q = 14,187. Four panels showing standard view, Dollard's four quadrants, hidden circulation ratio, and frequency response.</div>
  </div>

  <div class="two-col" style="margin-top: 20px;">
    <div>
      <h3>The Key Numbers</h3>
      <p>At the top of the coil: <span class="num">10,709x</span> more energy is CIRCULATING than FLOWING.</p>
      <p>At exact resonance frequency: <span class="num">13,097,635x</span> hidden circulation.</p>
    </div>
    <div>
      <h3>What This Means</h3>
      <p>Standard EE sees V(x) and I(x) sinusoids (top-left). Dollard shows WHERE energy stores, transfers, returns, and dissipates (top-right). The ratio (bottom-left) is the <em>operational picture</em> standard notation compresses away.</p>
    </div>
  </div>
  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      Tesla coil model: src/experiments/tesla_coil_four_quadrant.py:54-95<br>
      Four-quadrant computation: src/experiments/tesla_coil_four_quadrant.py:100-180<br>
      Energy map figure: src/experiments/dollard_key_plots.py:142-232
    </code>
  </div>
</div>

<!-- SLIDE 7: FIGURE 3 -->
<div class="slide" id="fig3">
  <h1>Figure 3: Profit Sheet vs Full Ledger</h1>
  <div class="figure">
    {img_tag('dollard_income_expenses', 'Income Expenses Analogy')}
    <div class="caption">The clearest way to explain the discovery: standard EE shows profit, Dollard shows the full ledger.</div>
  </div>

  <div class="highlight" style="margin-top: 30px;">
    <p class="big">It's the difference between knowing a company made $100K profit, and knowing it had $10M in revenue and $9.9M in expenses.</p>
    <p>The profit number is the same. The operational picture is completely different. A company with $100K profit on $200K revenue is healthy. A company with $100K profit on $10M revenue is stressed.</p>
  </div>

  <p style="margin-top: 20px;">At the top of the Tesla coil: storage (blue) = return (green) to many decimal places. The NET is near zero. The GROSS is enormous. <strong>The system is under immense internal stress that net measurement alone cannot see.</strong></p>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>Generated by: src/experiments/dollard_key_plots.py:235-296</code>
  </div>
</div>

<!-- SLIDE 8: THE NUMBERS -->
<div class="slide" id="numbers">
  <h1>The Numbers</h1>

  <table style="width: 100%; max-width: 900px;">
    <tr><th>Location on Coil</th><th>Net Energy</th><th>Gross Energy</th><th>Ratio</th><th>What Standard EE Sees</th></tr>
    <tr><td>Base (0%)</td><td>1.000</td><td>1.000</td><td class="num">1x</td><td>Full picture (gross = net)</td></tr>
    <tr><td>25%</td><td>0.781</td><td>1.303</td><td class="num">1.7x</td><td>Most of the picture</td></tr>
    <tr><td>50%</td><td>0.221</td><td>1.507</td><td class="num">6.8x</td><td>Missing 85% of activity</td></tr>
    <tr><td>75%</td><td>0.437</td><td>1.507</td><td class="num">3.4x</td><td>Missing 71% of activity</td></tr>
    <tr><td>Top (100%)</td><td>&asymp;0.000</td><td>1.507</td><td class="num">&rarr; infinity</td><td><span class="dead">BLIND</span> &mdash; sees nothing</td></tr>
  </table>

  <h3 style="margin-top: 30px;">Tesla Coil (Q = 14,187) at Resonance</h3>
  <table style="max-width: 900px;">
    <tr><th>Metric</th><th>Value</th><th>Source</th></tr>
    <tr><td>Gross/Net at coil top</td><td class="num">10,709x</td><td><code>tesla_coil_four_quadrant.py</code></td></tr>
    <tr><td>Gross/Net at resonant frequency</td><td class="num">13,097,635x</td><td><code>dollard_key_plots.py</code></td></tr>
    <tr><td>Quaternary identity error</td><td>&lt; 10<sup>-50</sup></td><td><code>tessarine_versor_verification.py</code></td></tr>
    <tr><td>Q factor</td><td>14,187</td><td><code>tesla_coil_four_quadrant.py:78</code></td></tr>
  </table>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      All numbers reproducible by running: python src/experiments/dollard_key_plots.py<br>
      Tesla coil model: python src/experiments/tesla_coil_four_quadrant.py<br>
      Full comparison: python src/experiments/dollard_vs_standard_comparison.py
    </code>
  </div>
</div>

<!-- SLIDE 9: N-PHASE CONNECTION -->
<div class="slide" id="connection">
  <h1>The N-Phase Connection</h1>
  <p>The quaternary decomposition is the <strong>same mathematical operation</strong> as the Fortescue/N-Phase decomposition.</p>

  <div class="two-col">
    <div>
      <h3>Quaternary (Dollard)</h3>
      <div class="math-block">
Group: Z&#8324; = {{1, j, -1, -j}}<br>
Acts on: Taylor series terms<br>
Grouping: power index mod 4<br>
Result: u, x, v, y
      </div>
    </div>
    <div>
      <h3>Fortescue (N-Phase)</h3>
      <div class="math-block">
Group: Z&#8345; = {{&omega;<sup>0</sup>, ..., &omega;<sup>N-1</sup>}}<br>
Acts on: Signal samples<br>
Grouping: DFT kernel &omega;<sup>ps</sup><br>
Result: N symmetrical components
      </div>
    </div>
  </div>

  <p style="margin-top: 20px;">For N=4, the Fortescue matrix uses 4th roots of unity {{1, i, -1, -i}} &mdash; exactly Dollard's {{1, j, h, k}}.</p>

  <div class="highlight">
    <p class="big">Both are Z&#8324;-indexed decompositions using 4th roots of unity. They differ only in DOMAIN: Dollard acts on power series terms, Fortescue acts on signal samples.</p>
  </div>

  <h3>Lean 4 Proof</h3>
  <div class="math-block">
<span style="color:#f0c040">theorem</span> four_phase_roots :<br>
&emsp;&emsp;omega4 ^ 0 = 1 &and;<br>
&emsp;&emsp;omega4 ^ 1 = Complex.I &and;<br>
&emsp;&emsp;omega4 ^ 2 = -1 &and;<br>
&emsp;&emsp;omega4 ^ 3 = -Complex.I
  </div>

  <div class="truth-box">
    <h4>Where Truth Lives</h4>
    <code>
      Lean proof: src/lean_proofs/polyphase/polyphase_formula.lean:202-236<br>
      N-Phase validation: 491 tests, N=2..12 (source_materials/N_PHASE_EVIDENCE.md)<br>
      Council analysis: research/council/dollard-pure-construction/03-analysis.md (Steps 7-8)<br>
      Paper 2: paper/paper2.tex:152-178 ("Character Decomposition from Fortescue to Cartan-Weyl")
    </code>
  </div>
</div>

<!-- SLIDE 10: PROVED vs DISCOVERED -->
<div class="slide" id="proved">
  <h1>What We Proved vs What We Discovered</h1>

  <div class="two-col">
    <div>
      <h3 style="color: #ff5050;">PROVED (Lean, zero sorry)</h3>
      <table>
        <tr><td>h = -1 forced by axioms</td><td class="dead">Z&#8324;</td></tr>
        <tr><td>Versor form ZY wrong</td><td class="dead">Disproved</td></tr>
        <tr><td>Algebra is cyclic group</td><td class="dead">Not 4D</td></tr>
        <tr><td>Tessarines &ne; Dollard</td><td class="dead">Refuted</td></tr>
        <tr><td>Polyphase = roots of unity</td><td class="alive">Standard</td></tr>
      </table>
    </div>
    <div>
      <h3 style="color: #50ff50;">DISCOVERED (Computation)</h3>
      <table>
        <tr><td>Gross/net ratio</td><td class="alive">Real metric</td></tr>
        <tr><td>10,709x at coil top</td><td class="alive">Computable</td></tr>
        <tr><td>Standard EE goes blind at resonance</td><td class="alive">Demonstrated</td></tr>
        <tr><td>Quaternary = Fortescue for N=4</td><td class="alive">Identity</td></tr>
        <tr><td>Bookkeeping value is real</td><td class="alive">Presentational</td></tr>
      </table>
    </div>
  </div>

  <div class="highlight" style="margin-top: 30px;">
    <p><strong>The algebra is dead.</strong> Z&#8324;, confirmed five ways. No new math.</p>
    <p><strong>The bookkeeping is alive.</strong> The gross/net ratio is a real, computable quantity that reveals structure standard notation compresses away. This is genuine value &mdash; presentational, not algebraic.</p>
  </div>
</div>

<!-- SLIDE 11: WHERE TRUTH LIVES -->
<div class="slide" id="truth">
  <h1>Where Truth Lives</h1>
  <p>Every claim in this presentation traces to a specific file.</p>

  <h3>Lean 4 Proofs (Machine-Verified)</h3>
  <table style="max-width: 900px;">
    <tr><th>Claim</th><th>File</th></tr>
    <tr><td>h = -1 forced (Z&#8324;)</td><td><code>src/lean_proofs/foundations/algebraic_necessity.lean</code></td></tr>
    <tr><td>Versor form sign error</td><td><code>src/lean_proofs/telegraph/telegraph_equation.lean</code></td></tr>
    <tr><td>Polyphase = roots of unity</td><td><code>src/lean_proofs/polyphase/polyphase_formula.lean</code></td></tr>
    <tr><td>Four-phase roots {{1, i, -1, -i}}</td><td><code>src/lean_proofs/polyphase/polyphase_formula.lean:202-236</code></td></tr>
    <tr><td>Cl(1,1) has jk &ne; 1</td><td><code>src/lean_proofs/clifford/cl11.lean</code></td></tr>
  </table>

  <h3>Computation Scripts (Python)</h3>
  <table style="max-width: 900px;">
    <tr><th>Script</th><th>What It Computes</th></tr>
    <tr><td><code>dollard_vs_standard_comparison.py</code></td><td>Quaternary decomposition, gross/net, transmission line analysis</td></tr>
    <tr><td><code>tesla_coil_four_quadrant.py</code></td><td>Tesla coil model, Q factor, four-quadrant energy map</td></tr>
    <tr><td><code>dollard_key_plots.py</code></td><td>Publication figures: core insight, energy map, income/expenses</td></tr>
    <tr><td><code>tessarine_versor_verification.py</code></td><td>Tessarine hypothesis refutation (9 tests)</td></tr>
    <tr><td><code>council/dollard_pure_construction_tests.py</code></td><td>Council Round 4 verification (4 tests)</td></tr>
  </table>

  <h3>Research Documents</h3>
  <table style="max-width: 900px;">
    <tr><th>Document</th><th>Content</th></tr>
    <tr><td><code>research/tessarine-discovery/00-synthesis</code></td><td>Master synthesis: proposed &amp; refuted in one session</td></tr>
    <tr><td><code>research/council/.../VERDICT.md</code></td><td>Council verdict: STOP. Algebra IS Z&#8324;. 92% confidence.</td></tr>
    <tr><td><code>research/council/.../06-over-unity-test-design.md</code></td><td>Full prediction space &amp; kill conditions (895 lines)</td></tr>
    <tr><td><code>research/council/.../03-analysis.md</code></td><td>Step-by-step reconstruction from epsilon</td></tr>
  </table>

  <h3>Figures</h3>
  <table style="max-width: 900px;">
    <tr><th>Figure</th><th>File</th></tr>
    <tr><td>Core insight (3 panels)</td><td><code>src/experiments/results/dollard_key_insight.png</code></td></tr>
    <tr><td>Tesla coil energy map (4 panels)</td><td><code>src/experiments/results/tesla_coil_energy_map.png</code></td></tr>
    <tr><td>Income/expenses analogy</td><td><code>src/experiments/results/dollard_income_expenses.png</code></td></tr>
    <tr><td>Dollard vs standard comparison</td><td><code>src/experiments/results/dollard_vs_standard.png</code></td></tr>
    <tr><td>Tesla coil standalone</td><td><code>src/experiments/results/tesla_coil_four_quadrant.png</code></td></tr>
  </table>

  <div class="highlight" style="margin-top: 30px;">
    <p><strong>Reproduce everything:</strong></p>
    <div class="math-block">
python src/experiments/dollard_vs_standard_comparison.py<br>
python src/experiments/tesla_coil_four_quadrant.py<br>
python src/experiments/dollard_key_plots.py<br>
python src/experiments/tessarine_versor_verification.py
    </div>
  </div>
</div>

<!-- SLIDE 12: OPEN QUESTIONS -->
<div class="slide">
  <h1>Open Questions</h1>

  <h3>1. Component Stress Prediction</h3>
  <p>Does high gross/net predict failure modes invisible to net-only analysis? A system with $100K profit on $10M revenue is under more internal stress than one with $100K profit on $200K revenue &mdash; even though the "profit" is identical.</p>

  <h3>2. N-Phase Harvesting</h3>
  <p>The quaternary expansion IS the N-Phase decomposition for N=4. The N-Phase system has 1,194 passing tests and a provisional patent. Can the gross/net metric be extracted from N-Phase decomposition outputs?</p>

  <h3>3. Diagnostic Instrumentation</h3>
  <p>Standard wattmeters show net real power. Standard VAR meters show reactive power magnitude. <strong>Neither shows the spatial distribution of energy cycling</strong> that the four-quadrant decomposition reveals. Is there a measurement that captures gross separately from net along a distributed system?</p>

  <div class="highlight" style="margin-top: 30px;">
    <p class="big">"Now that we can see what was invisible before, can we not harvest from what can now be seen?"</p>
    <p style="color: #999;">&mdash; Ian Michael Arnoldy, 2026-03-17</p>
  </div>
</div>

</body>
</html>"""

output_path = 'research/dollard-bookkeeping-discovery-presentation.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written: {output_path} ({len(html):,} bytes)")
print(f"Images embedded: {len(imgs)} figures as base64")
