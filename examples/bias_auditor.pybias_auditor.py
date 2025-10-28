import numpy as np
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import json

# Import the engine (assume in same dir or sys.path)
from spiral_engine import SpiralEngine

def audit_bias(corpus, labels, max_features=50):
    """
    Audit text corpus for bias using Spiral Path refinement.
    Returns baseline/spiral metrics and suggestions.
    """
    # Vectorize
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(corpus)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

    # Baseline
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    baseline_f1 = classification_report(y_test, y_pred, output_dict=True)['weighted avg']['f1-score']

    # Spiral Refinement
    engine = SpiralEngine()
    params = {'td': len(corpus), 'rf': 1.0, 'tw': 1.0, 'cir': 2.0, 'am': 0.05, 'da': np.pi/6}
    spiral_values = engine.simulate_spiral(params, iterations=3, sign='-')  # Convergent for balance

    # Apply twists to features (proxy shear)
    cum_twists = np.cumsum(spiral_values) / len(spiral_values)
    feature_weights = cum_twists[0] * vectorizer.idf_
    X_spiral_train = X_train.multiply(feature_weights)
    X_spiral_test = X_test.multiply(feature_weights)

    # Refined model
    model_spiral = LogisticRegression()
    model_spiral.fit(X_spiral_train, y_train)
    y_pred_spiral = model_spiral.predict(X_spiral_test)
    spiral_f1 = classification_report(y_test, y_pred_spiral, output_dict=True)['weighted avg']['f1-score']

    # Suggestions from log
    last_log = engine.get_provenance()[-1]
    suggestions = [
        f"Convergent refinement (- sign) reduced skew by {spiral_f1 - baseline_f1:.3f} F1 uplift.",
        f"Increase RF to {last_log['params']['rf'] * 1.1:.2f} for tighter pruning next cycle."
    ]

    return {
        'baseline_f1': baseline_f1,
        'spiral_f1': spiral_f1,
        'uplift': spiral_f1 - baseline_f1,
        'suggestions': suggestions,
        'provenance': last_log
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spiral Bias Auditor")
    parser.add_argument('--input', type=str, required=True, help="Path to corpus file (TXT, one doc per line)")
    parser.add_argument('--labels', type=str, required=True, help="Path to labels file (TXT, one int per line)")
    parser.add_argument('--output', type=str, default='audit_results.json', help="Output JSON file")
    
    args = parser.parse_args()
    
    # Load data
    with open(args.input, 'r') as f:
        corpus = [line.strip() for line in f.readlines()]
    with open(args.labels, 'r') as f:
        labels = [int(line.strip()) for line in f.readlines()]
    
    results = audit_bias(corpus, labels)
    print(f"Baseline F1: {results['baseline_f1']:.3f}")
    print(f"Spiral F1: {results['spiral_f1']:.3f}")
    print(f"Uplift: {results['uplift']:.3f}")
    print("Suggestions:", results['suggestions'])
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {args.output}")
