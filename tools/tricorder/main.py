#!/usr/bin/env python3
"""
Spiral Path Tricorder CLI: Probe contexts, forge chains.
Usage: python main.py "debug latency" --domain tech --max_iters 3 --output json --viz
"""

import argparse
import json
import os
from typing import Dict
import matplotlib.pyplot as plt
import networkx as nx
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
    parser.add_argument('--viz', action='store_true', 
                        help='Generate PNG graph viz of chains (saves to outputs/).')
    return parser.parse_args()

def render_result(result: Dict, fmt: str = 'text') -> str:
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

def generate_viz(chains: Dict, filename: str = 'chain_graph.png'):
    """Viz: NetworkX graph of chains, colored by weight."""
    G = nx.DiGraph()
    
    # Primary chain
    for i, edge in enumerate(chains['primary_chain']):
        src, tgt, wt = edge
        G.add_edge(src, tgt, weight=wt, color='green' if wt > 0.7 else 'yellow')
    
    # Poetic fork
    for fork in chains['poetic_fork']:
        node, rel, wt = fork['node'], fork['rel'], fork['weight']
        G.add_edge(node, rel, weight=wt, color='blue' if wt > 0.8 else 'orange')
    
    pos = nx.spring_layout(G)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    weights = [G[u][v]['weight'] * 5 for u, v in G.edges()]  # Scale for viz
    
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
    result = tricorder_scan(args.seed, args.domain, args.max_iters)
    result['domain'] = args.domain  # Stamp for render
    
    print(render_result(result, args.output))
    
    if args.viz:
        os.makedirs('outputs', exist_ok=True)
        viz_file = f"outputs/{args.seed.replace(' ', '_')}_chains.png"
        chains = result['chains']
        generate_viz(chains, viz_file)
        print(f"\nViz saved: {viz_file}")

if __name__ == "__main__":
    main()
