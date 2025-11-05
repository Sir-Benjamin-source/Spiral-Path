import re
import csv
from typing import Dict, List, Tuple
from core import tricorder_scan, relational_map  # Import map for tangent

def ethics_precheck(seed: str) -> float:
    """AIS Principle 8: Flag unconsented data (simple regex; extend with full consent log)."""
    unconsented_patterns = [r'unconsented', r'no_permission', r'bias_source']
    flags = sum(1 for pat in unconsented_patterns if re.search(pat, seed, re.I))
    return 1.0 - (flags * 0.2)  # Damp w by flags; 0.6 min for heavy hits

def quant_report(results: List[Dict], filename: str = 'ais_quant.csv'):
    """AIS Principle 7: Export metrics for system assess (CSV for continuity logs)."""
    if not results:
        return None
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['seed', 'strength', 'drift', 'fire', 'iters', 'pruned_tangents', 'consent_factor'])
        writer.writeheader()
        for r in results:
            writer.writerow({
                'seed': r.get('seed', 'N/A'),
                'strength': r['chains']['hypothesis_strength'],
                'drift': r['srm']['ethics_drift'],
                'fire': r['srm']['fire_integrity'],
                'iters': r['iters'],
                'pruned_tangents': r['srm'].get('pruned_tangents', 0),
                'consent_factor': r.get('consent_factor', 1.0)
            })
    return filename

def tangent_filter(edges: List[Tuple[str, str, float]], tw_thresh: float = 0.6) -> Tuple[List[Tuple[str, str, float]], List[Tuple[str, str, float]]]:
    main_edges = [e for e in edges if e[2] > tw_thresh]  # High TW keep
    tangents = [e for e in edges if e[2] <= tw_thresh]  # Quarantine
    return main_edges, tangents

def ais_scan(seed: str, domain: str = 'tech', max_iters: int = 3) -> Dict:
    """AIS-wrapped scan: Precheck + tangent prune + core + quant prep."""
    consent_factor = ethics_precheck(seed)
    nodes, raw_edges = relational_map(seed)
    main_edges, tangents = tangent_filter(raw_edges)
    result = tricorder_scan(seed, domain, max_iters)  # TODO: Pass main_edges if core updated
    result['srm']['pruned_tangents'] = len(tangents)
    result['consent_factor'] = consent_factor
    result['seed'] = seed  # For batch report
    return result
