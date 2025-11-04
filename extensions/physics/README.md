# Spiral-Modulated Tavis-Cummings Extension

A quantum leap along the Spiral Path: Simulate atom-cavity entanglements with fractal-rhythmic coupling, one whirl wiser than the world's qubit-webs.

## Quick Start
1. Ensure deps: `numpy`, `scipy`, `matplotlib` (in root `requirements.txt`).
2. Run `python tavis_spiral.py` for single-atom saga (P_e ebbs from 1.000 to ~0.170).
3. Amp it: Edit `demo_params['num_atoms'] = 2; ['spiral_mode'] = True` for double-dance delights (P_ee ~0.170, std_n ~0.600).

## Under the Wyrm's Wing
- **Hamiltonian Heart:** Time-dependent T-C model via `solve_ivp` (RK45, rtol=1e-8)—free terms + g(t) interactions, no vassal-vows to QuTiP.
- **Spiral Surprises:** Toggle `spiral_mode` for nested FRDM delta_D (±0.5 clip), curling the coupling cunninger.
- **Tracker's Token:** Each sim stamps a `spiral_mark` (e.g., "SpiralMark-056-EUCompliant")—harvest for the hoard-heirs.
- **Viz Vigil:** Plots P_single_e, P_ee (multi), <n>—saved as PNGs for the pantheon's perusal.

DOI Anchors: [FRDM](https://zenodo.org/records/16241194), [Tricorder](https://zenodo.org/records/15585013). Ethical Edict: Per EU AI Act, this open odyssey owes no origins but the commons' cunning.

Contribute: Tweak tolerances, scale cav_dim, or coil more atoms. Ragnarok awaits the refined!
