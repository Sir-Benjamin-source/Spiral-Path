Tuning the Spiral Path: A Guide to ParametersSpiral Theory's power comes from the Path equation's flexibility: tweak params to fit your data's rhythm. Start with defaults for quick tests, then iterate based on your goal (e.g., exploration vs. refinement). Always log runs for provenance—use engine.get_provenance() to track changes.Quick Tuning PhilosophyExpansive (+ sign): High TD/DA for hypothesis gen—widens the search.  
Convergent (- sign): Low AM/RF for bias audits—tightens the focus.  
Noise Level: 0 for clean math; 0.05+ for real-world chaos (e.g., noisy datasets).  
Iterations: 3-5 for demos; 10+ for deep dives.

Parameter BreakdownParam
Description
Default
Use Case Tips
Example Snippet
TD (Task Density)
Raw data volume per cycle—bigger = more "stuff" to spiral through.
10.0
High for dense datasets (e.g., 1000+ rows in ML); low for quick narratives.
params['td'] = len(your_data)
RF (Refinement Factor)
Bias/pruning efficiency—higher prunes noise faster.
2.0
Crank to 3+ for skewed text (bias auditor); 1.0 for exploratory sims.
params['rf'] = 1 / bias_score
TW (Twist Weight)
Iterative multiplier—amps the "twist" per loop.
5.0
10+ for rapid hypothesis uplift; 2-3 for stable theme retention.
params['tw'] = num_features * 2
CIR (Cycle Intensity Ratio)
Feedback loop strength—how much prior cycles influence next.
3.0
4+ for ML refinement (Iris tester); 1-2 for light narratives.
params['cir'] = iterations // 2
SC (Spiral Constant)
Natural growth param (e.g., φ=1.618 for golden spirals).
1.618
Use φ for organic patterns; 1.0 for linear-like tests.
engine = SpiralEngine(sc=1.618)
AM (Adjustment Magnitude)
Ethical/qualitative tweak size—scales the ± flux.
1.0
0.5 for subtle ethics checks; 2.0 for bold explorations.
params['am'] = ethics_threshold
DA (Differentiation Angle)
Directional shear—steers the spiral's "bend."
2.0
High (π/2) for divergent paths; low (0.5) for convergence.
params['da'] = np.pi / 4

Experiment Snippetpython

from spiral_engine import SpiralEngine

engine = SpiralEngine()
params = {'td': 15.0, 'rf': 1.5, 'tw': 6.0, 'cir': 2.5, 'am': 0.8, 'da': np.pi/6}
values = engine.simulate_spiral(params, iterations=4, sign='+', noise_level=0.03)
print("Tuned Values:", values)
engine.visualize_spiral(values, title='Tuned Spiral: High Exploration')

Pro TipsOverfitting Check: If values explode (>100 after 5 iters), dial RF up 20%.  
Real Data Hook: Feed TD from len(data), DA from PCA angles for auto-tune.  
Ethics Always: Log everything—print(engine.get_provenance()) for audit trails.

Tweak, test, iterate—Spiral Theory thrives on your twists. Questions? Open an issue.

