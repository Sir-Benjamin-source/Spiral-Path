# Spiral Path Tricorder

Tool for iterative context navigation using Spiral Path eq + SRM ethics.

## Usage
pip install -e .  # From tools/
python tricorder/main.py "your seed" --domain tech --ais --viz

Domains: tech (debug), poetic (rhyme hunt), research (hypo refine).
Args: --max_iters 5, --td_max 3, --seeds file.txt (batch AIS).

## Equation Ref
S_{n+1} = S_n + α(E · ∇R) + β A(ΔC)
- E: Exploration (domain-boosted).
- ∇R: Relevance grad (cosine proxy).
- A: Adjustment (log damp).

## Examples
- Tech: "debug latency" → Chains latency → CPU, strength 1.28, CSV quant.
- Poetic: "nature beauty" → Fork to "divine fire", viz PNG.
- Research: "coral reef impacts" → Pruned tangents=2, drift=0.98.

Ethical: AIS prechecks consent; see A.I.S. Standard DOI.

License: MIT. DOI Target: zenodo.org/deposit (upload this dir).
