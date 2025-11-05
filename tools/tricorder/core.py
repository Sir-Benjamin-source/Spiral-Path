import numpy as np
from typing import Dict, List, Tuple
from functools import lru_cache  # Cache for efficiency
import networkx as nx  # Already in viz; reuse

@lru_cache(maxsize=128)
def relational_map(context_seed: str, td_max: int = 3) -> Tuple[List[str], List[Tuple[str, str, float]]]:
    words = context_seed.lower().split()
    G = nx.Graph()
    G.add_edges_from([(words[i], words[i+1], {'weight': 0.8}) for i in range(len(words)-1)])
    edges = []
    for node in set(words):
        neighbors = list(nx.single_source_shortest_path(G, node, cutoff=td_max).items())
        for tgt, path in neighbors:
            if len(path) <= td_max + 1:  # Hop limit
                edges.append((node, tgt, 0.8))
    return list(set(words)), edges[:20]  # Final cap

def init_vector(nodes: List[str]) -> np.ndarray:
    return np.array([1.0, 0.0, 0.0])

def explore_factor(edges: List[Tuple[str, str, float]], domain: str) -> float:
    base = 0.3
    return base + (0.2 if domain == 'poetic' else 0.1)

def relevance_grad(state: np.ndarray, edges: List[Tuple[str, str, float]]) -> np.ndarray:
    return np.array([0.5 * len(edges)/5.0, 0.2, -0.1 * state[2]])

def adjust_pert(state: np.ndarray, new_insights: str) -> np.ndarray:
    pert_mag = -np.log(1 + len("neutral_perturbation")) * 0.1
    return np.array([0.0, pert_mag, 0.0])

def update_spiral(state: np.ndarray, E: float, grad_R: np.ndarray, A: np.ndarray) -> np.ndarray:
    alpha, beta = 0.7, 0.3
    return state + alpha * (E * grad_R) + beta * A

def convergence(state: np.ndarray) -> float:
    return min(1.0, np.linalg.norm(state[:2]) / np.sqrt(2))

def build_output(state: np.ndarray, edges: List[Tuple[str, str, float]]) -> Dict:
    return {
        "primary_chain": edges[:3],
        "poetic_fork": [{"node": e[0], "rel": e[1], "weight": e[2]} for e in edges[2:4]],
        "hypothesis_strength": float(state[0])
    }

def tricorder_scan(context_seed: str, domain: str = 'tech', max_iters: int = 3) -> Dict:  # Default 3 for speed
    nodes, edges = relational_map(context_seed)
    state = init_vector(nodes)
    new_insights = "neutral_perturbation"
    
for i in range(max_iters):
    E = explore_factor(edges, domain)
    grad_R = relevance_grad(state, edges)
    rf_thresh = 0.5  # Tune; higher for strict mitigation
    edges = [e for e in edges if e[2] * grad_R[0] > rf_thresh]  # Prune low-RF
    A = adjust_pert(state, new_insights)
    state = update_spiral(state, E, grad_R, A)
    if convergence(state) > 0.85:
        break
    
    chains = build_output(state, edges)
    srm = {"ethics_drift": min(1.0, 1 - abs(state[2])), "fire_integrity": float(state[0])}
    return {"chains": chains, "srm": srm, "iters": i + 1}
