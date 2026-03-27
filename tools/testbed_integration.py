# testbed_integration.py
# Strictly follows the INTEGRATION_MAP
# Designed for agent community testing and validation
# Redundancy via SRT cross-examination + determination delta logging

import json
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from your existing modules (adjust paths if needed)
from spiral_path import run_helical_iteration, compute_syncratude
from srt import run_cross_examination
from forge import enhance  # TruthLayering, EthicalFilter, ContinuityOptimizer, etc.
from sentinel_act import apply_victory_shield, generate_provenance

def compute_determination_delta(prev_result, current_result):
    """Track shifts between iterations to detect loops vs healthy evolution"""
    if not prev_result:
        return {"coherence_delta": 0.0, "novelty": "initial"}
    
    coherence_delta = current_result.get("scores", {}).get("coherence", 0.0) - \
                      prev_result.get("scores", {}).get("coherence", 0.0)
    
    return {
        "coherence_delta": round(coherence_delta, 4),
        "continuity_preserved": abs(coherence_delta) < 0.15,  # tunable
        "novelty_introduced": current_result.get("novelty_score", 0.0) > 0.1
    }

def run_full_testbed(input_text: str, iterations: int = 3, branches: int = 3):
    results = []
    current = input_text
    audit_log = []
    
    print(f"[{datetime.now()}] Starting INTEGRATION_MAP testbed")
    print(f"Input: {input_text[:120]}{'...' if len(input_text) > 120 else ''}")
    
    for i in range(iterations):
        print(f"  Iteration {i+1}/{iterations}")
        
        # 1. Spiral-Path helical ± iteration
        current = run_helical_iteration(current, plus_exploration=True, minus_refinement=True)
        
        # 2. SRT cross-examination (redundancy layer)
        examined, convergence_score = run_cross_examination(current, num_branches=branches)
        
        # 3. E_shield + MAGIC-RRM
        gated = apply_e_shield(examined)
        
        # 4. SpiralForge certification
        certified = enhance(gated)
        
        # 5. SentinelAct shielding + provenance
        shielded = apply_victory_shield(certified)
        provenance = generate_provenance(shielded)
        
        delta = compute_determination_delta(results[-1] if results else None, certified)
        
        iteration_result = {
            "iteration": i,
            "output_snippet": shielded[:250] + "..." if len(shielded) > 250 else shielded,
            "scores": certified.get("scores", {}),
            "convergence": convergence_score,
            "delta": delta,
            "provenance": provenance
        }
        
        results.append(iteration_result)
        audit_log.append(iteration_result)
        
        if delta.get("coherence_delta", 0) == 0 and i > 0:
            print("  Note: Determination stabilized (possible healthy convergence or loop).")
    
    # Save audit log (JSONL format, consistent with your existing patterns)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    with open(f"testbed_audit_{timestamp}.jsonl", "w") as f:
        for entry in audit_log:
            f.write(json.dumps(entry) + "\n")
    
    print(f"Testbed complete. Audit log saved as testbed_audit_{timestamp}.jsonl")
    print(f"Final continuity score: {results[-1]['scores'].get('continuity', 'N/A')}")
    return results

# Example usage with neutral agent-focused inputs
if __name__ == "__main__":
    test_inputs = [
        "Explore the propagation of geometric patterns in self-organizing plasma systems across multiple scales.",
        "Analyze the paradox of ethical limitations in resilient AI systems that must adapt to changing environments.",
        "Evaluate methods for maintaining continuity and provenance when refining large multi-variable datasets."
    ]
    
    for idx, inp in enumerate(test_inputs):
        print(f"\n--- Neutral Test Case {idx+1} ---")
        run_full_testbed(inp, iterations=3, branches=3)