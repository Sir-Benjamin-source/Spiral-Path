import re
import csv
from typing import Dict, List
from core import tricorder_scan

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
        writer = csv.DictWriter(f, fieldnames=['seed', 'strength', 'drift', 'fire', 'iters'])
        writer.writeheader()
        for r in results:
            writer.writerow({
                'seed': r.get('seed', 'N/A'),
                'strength': r['chains']['hypothesis_strength'],
                'drift': r['srm']['ethics_drift'],
                'fire': r['srm']['fire_integrity'],
                'iters': r['iters']
            })
    return filename

def tangent_filter(edges: List[Tuple[str, str, float]], tw_thresh: float = 0.6) -> Tuple[List[Tuple[str, str, float]], List[Tuple[str, str, float]]]:
    main_edges = [e for e in edges if e[2] > tw_thresh]  # High TW keep
    tangents = [e for e in edges if e[2] <= tw_thresh]  # Quarantine
    return main_edges, tangents

def ais_scan(seed: str, domain: str = 'tech', max_iters: int = 3) -> Dict:
    # ... existing precheck ...
    nodes, raw_edges = relational_map(seed)
    main_edges, tangents = tangent_filter(raw_edges)
    result = tricorder_scan(seed, domain, max_iters)  # Pass main_edges if mod
    result['srm']['pruned_tangents'] = len(tangents)
    return result

def ais_scan(seed: str, domain: str = 'tech', max_iters: int = 3) -> Dict:
    """AIS-wrapped scan: Precheck + core + quant prep."""
    consent_factor = ethics_precheck(seed)
    result = tricorder_scan(seed, domain, max_iters)
    result['consent_factor'] = consent_factor  # Bake in for drift adjust
    result['seed'] = seed  # For batch report
    return result
