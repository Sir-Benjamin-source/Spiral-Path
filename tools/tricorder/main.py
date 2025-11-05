#!/usr/bin/env python3
"""
Spiral Path Tricorder CLI: Probe contexts, forge chains.
Usage: python main.py "debug latency" --domain tech --max_iters 3 --output json
"""

import argparse
import json
from core import tricorder_scan  # Core engine; assume in same dir or sys.path

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tricorder: Spiral-scan contexts for relational chains & SRM insights.',
        epilog='Ethical note: Anchors in A.I.S. reality; consent-checked at inflow.'
    )
    parser.add_argument('seed', type=str, help='Context seed (query/text/dataset snippet).')
    parser.add_argument('--domain', type=str, default='tech', 
                        choices=['tech', 'poetic', 'research'], 
                        help='Scan domain (default: tech).')
    parser.add_argument('--max_iters', type=int, default=5, 
                        help='Max spiral iterations (default: 5).')
    parser.add_argument('--output', type=str, default='text', 
                        choices=['text', 'json'], 
                        help='Output format (default: text).')
    return parser.parse_args()

def render_result(result, fmt='text'):
    if fmt == 'json':
        return json.dumps(result, indent=2)
    else:
        chains = result['chains']
        srm = result['srm']
        iters = result['iters']
        out = f"=== Tricorder Scan Results ===\n"
        out += f"Seed Domain: {result.get('domain', 'unspecified')}\n"
        out += f"Iterations: {iters}\n\n"
        out += "Primary Chains:\n"
        for edge in chains['primary_chain']:
            out += f"  {edge[0]} → {edge[1]} (w: {edge[2]})\n"
        out += "\nPoetic/Alt Fork:\n"
        for fork in chains['poetic_fork']:
            out += f"  {fork['node']} → {fork['rel']} (w: {fork['weight']})\n"
        out += f"\nHypothesis Strength: {chains['hypothesis_strength']:.2f}\n"
        out += f"SRM Ethics Drift: {srm['ethics_drift']:.2f} (lower better)\n"
        out += f"Fire Integrity: {srm['fire_integrity']:.2f} (higher thirstier)\n"
        return out

def main():
    args = parse_args()
    result = tricorder_scan(args.seed, args.domain, args.max_iters)
    result['domain'] = args.domain  # Stamp for render
    print(render_result(result, args.output))

if __name__ == "__main__":
    main()
