import numpy as np
from typing import Dict, List, Tuple

def relational_map(context_seed: str) -> Tuple[List[str], List[Tuple[str, str, float]]]:
    """Extract nodes/edges via basic relational meaning map (SRM-weighted)."""
    words = context_seed.lower().split()
    nodes = list(set(words))
    edges = [(words[i], words[i+1], 0.8) for i in range(len(words)-1)]  # Placeholder; hook to full SRM later
    return nodes, edges

def init_vector(nodes: List[str]) -> np.ndarray:
    """Init state: [strength, depth, bias]."""
    return np.array([1.0, 0.0, 0.0])

def explore_factor(edges: List[Tuple[str, str, float]], domain: str) -> float:
    """E: Domain-boosted exploration (poetic gets +0.2 for resonance)."""
    base = 0.3
    return base + (0.2 if domain == 'poetic' else 0.1)

def relevance_grad(state: np.ndarray, edges: List[Tuple[str, str, float]]) -> np.ndarray:
    """∇R: Cosine-sim proxy on edges (dummy vector; scale with real embeddings)."""
    return np.array([0.5 * len(edges)/5.0, 0.2, -0.1 * state[2]])  # Bias-damped

def adjust_pert(state: np.ndarray, new_insights: str) -> np.ndarray:
    """A(ΔC): Vector damp on perturbations (log decay for stability)."""
    pert_mag = -np.log(1 + len(new_insights or '')) * 0.1
    return np.array([0.0, pert_mag, 0.0])  # Depth nudge, ethics anchor

def update_spiral(state: np.ndarray, E: float, grad_R: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Core Spiral Path: S_{n+1} = S_n + α(E · ∇R) + β A(ΔC)."""
    alpha, beta = 0.7, 0.3  # Tunables; SRM auto-scales β on ethical drift
    return state + alpha * (E * grad_R) + beta * A

def convergence(state: np.ndarray) -> float:
    """Check: Norm on [strength, depth] > thresh (capped at 1.0)."""
    return min(1.0, np.linalg.norm(state[:2]) / np.sqrt(2))

def build_output(state: np.ndarray, edges: List[Tuple[str, str, float]]) -> Dict:
    """Lens: Chains + score (JSON-ready for supps)."""
    return {
        "primary_chain": edges[:3],
        "poetic_fork": [{"node": e[0], "rel": e[1], "weight": e[2]} for e in edges[2:4]],  # Tease alt
        "hypothesis_strength": float(state[0])
    }

def tricorder_scan(context_seed: str, domain: str = 'tech', max_iters: int = 5) -> Dict:
    """Full scan: Input seed → Spiral chains + SRM score."""
    nodes, edges = relational_map(context_seed)
    state = init_vector(nodes)
    new_insights = context_seed  # Self-pert for demo; real: external ΔC
    
    for _ in range(max_iters):
        E = explore_factor(edges, domain)
        grad_R = relevance_grad(state, edges)
        A = adjust_pert(state, new_insights)
        state = update_spiral(state, E, grad_R, A)
        if convergence(state) > 0.85:
            break  # Early quench on thirst met
    
    chains = build_output(state, edges)
    srm = {"ethics_drift": min(1.0, 1 - abs(state[2])), "fire_integrity": float(state[0])}  # Living word proxy
    return {"chains": chains, "srm": srm, "iters": _ + 1}

# Demo hook (for main.py CLI)
if __name__ == "__main__":
    print(tricorder_scan("debug latency in software poetic rhymes", domain='poetic'))
