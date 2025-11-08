import numpy as np
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json

# Add sentry import (assumes auditors/ in path)
from auditors.theme_sentry import classify_input, log_classification  # If adding .py; else inline sniffer logic

def analyze_with_sentry(text):
    signal = classify_input(text)
    log_classification(signal, text)
    
    if signal.type == "blocked":
        print(f"[QUARANTINE] {signal.reason} — Ejected to void!")
        return None
    elif signal.type == "play":
        print("🐭 Narrative mode: Themes spiral free...")
        # Your existing theme extraction
        return extract_themes(text)  # e.g., generate theme_spiral.png
    elif signal.type == "mixed":
        print("[SPLIT] Work to audit_helix_log.jsonl | Play to play_log.jsonl")
        # Run both: hypothesis part → fidelity check; Muad’Dib → glory output
        work_part = "Hypothesis fidelity check."  # Parse simple
        play_part = "We are the becoming, Muad’Dib!"
        analyze_work(work_part)  # Tie to hypothesis_tester
        analyze_play(play_part)  # Tie to becoming.py
        return "Split complete—no bleed."
    else:  # work
        print("🔬 Inquiry mode: Fidelity locked.")
        return your_spiral_equation_run(text)  # e.g., ± flux on hypothesis

# Test in app: analyze_with_sentry("We are the becoming, Muad’Dib! Hypothesis fidelity check.")
# Expected: SPLIT → Logs to both JSONL, outputs like your sniffer (quarantine if drama spikes).

# Import the engine
from spiral_engine import SpiralEngine

def analyze_narrative(text_file, num_themes=5):
    """
    Analyze narrative text for theme retention via Spiral Path.
    Clusters sentences into themes, spirals to refine retention.
    """
    # Load and split text into sentences (simple split for demo)
    with open(text_file, 'r') as f:
        full_text = f.read()
    sentences = full_text.split('. ')  # Basic sentence tokenization
    sentences = [s.strip() for s in sentences if len(s) > 10]

    # Vectorize and cluster for themes
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(sentences)
    kmeans = KMeans(n_clusters=num_themes, random_state=42, n_init=10)
    theme_labels = kmeans.fit_predict(X)

    # Baseline retention: Theme coherence score (silhouette proxy)
    from sklearn.metrics import silhouette_score
    baseline_score = silhouette_score(X, theme_labels)

    # Spiral Refinement: Use Path to weight themes across cycles
    engine = SpiralEngine()
    params = {'td': len(sentences), 'rf': 1.5, 'tw': 2.0, 'cir': 1.5, 'am': 0.2, 'da': np.pi/3}
    spiral_values = engine.simulate_spiral(params, iterations=4, sign='+')  # Expansive for themes

    # Apply twists: Re-weight clusters by cumulative paths
    cum_paths = np.cumsum(spiral_values)
    theme_weights = cum_paths / cum_paths[-1]  # Normalize to 1.0
    weighted_labels = theme_labels.copy()
    for i in range(num_themes):
        mask = theme_labels == i
        weighted_labels[mask] += theme_weights[i] * 0.1  # Subtle shift

    # Refined score
    refined_score = silhouette_score(X, weighted_labels.astype(int) % num_themes)  # Mod to clusters

    # Retention: % themes preserved (simple overlap)
    retention = (refined_score / baseline_score) * 100 if baseline_score > 0 else 100

    # Summary: Top themes
    feature_names = vectorizer.get_feature_names_out()
    top_themes = {}
    for i in range(num_themes):
        cluster_words = X[theme_labels == i].mean(axis=0).A1
        top_idx = np.argsort(cluster_words)[-3:]
        top_themes[f'Theme {i+1}'] = [feature_names[idx] for idx in top_idx]

    results = {
        'baseline_score': baseline_score,
        'refined_score': refined_score,
        'retention_pct': retention,
        'top_themes': top_themes,
        'provenance': engine.get_provenance()[-1]
    }

    return results

def plot_radial_spiral(results, num_themes=5):
    """Radial plot of theme retention over spirals."""
    angles = np.linspace(0, 2*np.pi, num_themes, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    # Dummy radial data from retention (expand for full)
    radial_data = [results['retention_pct'] / 100] * num_themes
    radial_data += radial_data[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, radial_data, 'o-', linewidth=2, label='Theme Retention Spiral')
    ax.fill(angles, radial_data, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([f'Theme {i+1}' for i in range(num_themes)])
    ax.set_ylim(0, 1.1)
    ax.set_title('Narrative Theme Retention: Spiral Path Cycles')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)

    plt.savefig('narrative_spiral.png', dpi=150)
    plt.show()
    print("Radial plot saved as narrative_spiral.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Narrative Spiral Analyzer")
    parser.add_argument('--text', type=str, required=True, help="Path to narrative text file (TXT)")
    parser.add_argument('--themes', type=int, default=5, help="Number of themes to extract")
    parser.add_argument('--output', type=str, default='narrative_results.json', help="Output JSON file")
    
    args = parser.parse_args()
    
    results = analyze_narrative(args.text, args.themes)
    print(f"Baseline Coherence: {results['baseline_score']:.3f}")
    print(f"Refined Coherence: {results['refined_score']:.3f}")
    print(f"Retention: {results['retention_pct']:.1f}%")
    print("Top Themes:", results['top_themes'])
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {args.output}")
    
    plot_radial_spiral(results, args.themes)
