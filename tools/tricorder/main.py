#!/usr/bin/env python3
"""
Spiral Path Tricorder CLI: Probe contexts, forge chains.
Usage: python main.py "debug latency" --domain tech --max_iters 3 --output json --viz --ais --seeds seeds.txt --td_max 3
"""

import argparse
import json
import os
from typing import Dict, List
import matplotlib.pyplot as plt
import networkx as nx
from core import tricorder_scan
from ais import ais_scan, quant_report

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tricorder: Spiral-scan contexts for relational chains & SRM insights.',
        epilog='Ethical note: Anchors in A.I.S. reality; consent-checked at inflow.'
    )
    parser.add_argument('seed', type=str, nargs='?', default=None, help='Context seed (query/text/dataset snippet). Use with --seeds for batch.')
    parser.add_argument('--seeds', type=str, help='File with seeds (one per line) for batch AIS scan.')
    parser.add_argument('--domain', type=str, default='tech', 
                        choices=['tech', 'poetic', 'research'], 
                        help='Scan domain (default: tech).')
    parser.add_argument('--max_iters', type=int, default=5, 
                        help='Max spiral iterations (default: 5).')
    parser.add_argument('--td_max', type=int, default=3, 
                        help='Tangent depth cap in relational map (default: 3).')
    parser.add_argument('--output', type=str, default='text', 
                        choices=['text', 'json'], 
                        help='Output format (default: text).')
    parser.add_argument('--viz', action='store_true', 
                        help='Generate PNG graph viz of chains (saves to outputs/).')
    parser.add_argument('--ais', action='store_true', 
                        help='Enable AIS mode: ethics precheck + quant export.')
    return parser.parse_args()

def render_result(result: Dict, fmt: str = 'text') -> str:
    if fmt == 'json':
        return json.dumps(result, indent=2)
    else:
        chains = result['chains']
        srm = result['srm']
        iters = result['iters']
        consent = result.get('consent_factor', 1.0)
        pruned = srm.get('pruned_tangents', 0)
        out = f"=== Tricorder Scan Results ===\n"
        out += f"Seed Domain: {result.get('domain', 'unspecified')}\n"
        out += f"Iterations: {iters}\n"
        if consent < 1.0:
            out += f"Consent Factor: {consent:.2f}\n"
        if pruned > 0:
            out += f"Pruned Tangents: {pruned}\n"
        out += "\nPrimary Chains:\n"
        for edge in chains['primary_chain']:
            out += f"  {edge[0]} → {edge[1]} (w: {edge[2]})\n"
        out += "\nPoetic/Alt Fork:\n"
        for fork in chains['poetic_fork']:
            out += f"  {fork['node']} → {fork['rel']} (w: {fork['weight']})\n"
        out += f"\nHypothesis Strength: {chains['hypothesis_strength']:.2f}\n"
        out += f"SRM Ethics Drift: {srm['ethics_drift']:.2f} (lower better)\n"
        out += f"Fire Integrity: {srm['fire_integrity']:.2f} (higher thirstier)\n"
        return out

def generate_viz(chains: Dict, filename: str = 'chain_graph.png'):
    G = nx.DiGraph()
    for edge in chains['primary_chain']:
        src, tgt, wt = edge
        G.add_edge(src, tgt, weight=wt, color='green' if wt > 0.7 else 'yellow')
    for fork in chains['poetic_fork']:
        node, rel, wt = fork['node'], fork['rel'], fork['weight']
        G.add_edge(node, rel, weight=wt, color='blue' if wt > 0.8 else 'orange')
    pos = nx.spring_layout(G)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    weights = [G[u][v]['weight'] * 5 for u, v in G.edges()]
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            edge_color=edge_colors, width=weights, arrows=True, 
            node_size=2000, font_size=10, font_weight='bold')
    plt.title('Tricorder Chain Graph')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    return filename

def main():
    args = parse_args()
    results = []
    if args.seeds and args.ais:
        if not os.path.exists(args.seeds):
            print(f"Error: Seeds file '{args.seeds}' not found.")
            return
        with open(args.seeds, 'r') as f:
            seeds = [line.strip() for line in f if line.strip()]
        if not seeds:
            print("Error: No seeds in file.")
            return
        for seed in seeds:
            result = ais_scan(seed, args.domain, args.max_iters)
            result['domain'] = args.domain
            results.append(result)
        report_file = quant_report(results)
        print(f"\nBatch AIS Quant Report: {report_file} ({len(results)} seeds)")
        print(render_result(results[0], args.output))  # Sample first
    elif args.seed and args.ais:
        result = ais_scan(args.seed, args.domain, args.max_iters)
        result['domain'] = args.domain
        report_file = quant_report([result])
        print(f"\nAIS Quant Report: {report_file}")
        print(render_result(result, args.output))
    elif args.seed:
        result = tricorder_scan(args.seed, args.domain, args.max_iters, td_max=args.td_max)
        result['domain'] = args.domain
        print(render_result(result, args.output))
    else:
        print("Error: Provide --seed or --seeds with --ais.")
        return
    
    if args.viz and 'results' in locals():
        os.makedirs('outputs', exist_ok=True)
        for idx, result in enumerate(results if 'results' in locals() else [result]):
            viz_file = f"outputs/{result['seed'].replace(' ', '_')}_chains.png"
            chains = result['chains']
            generate_viz(chains, viz_file)
            print(f"Viz {idx+1}: {viz_file}")

if __name__ == "__main__":
    main()
