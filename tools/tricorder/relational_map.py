# Light copy for standalone use; import from core in full suite
from functools import lru_cache
import networkx as nx
from typing import Tuple, List

@lru_cache(maxsize=128)
def relational_map(context_seed: str, td_max: int = 3) -> Tuple[List[str], List[Tuple[str, str, float]]]:
    words = context_seed.lower().split()
    G = nx.Graph()
    G.add_edges_from([(words[i], words[i+1], {'weight': 0.8}) for i in range(len(words)-1)])
    edges = []
    for node in set(words):
        neighbors = list(nx.single_source_shortest_path(G, node, cutoff=td_max).items())
        for tgt, path in neighbors:
            if len(path) <= td_max + 1:
                edges.append((node, tgt, 0.8))
    return list(set(words)), edges[:10]
