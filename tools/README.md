# Tools Directory

This `tools/` directory contains practical utilities and diagnostic aids for the **Spiral-Path** helical iteration engine and the broader **Spiral Codex** ecosystem.

These tools support agent-centric workflows: validating the **INTEGRATION_MAP**, ensuring continuity, enforcing ethical gating, and measuring refinement quality without external dependencies.

## Contents

- **`tricorder/`** — Diagnostic and scanning utilities (demo_tricorder.py and related modules). Used for general inspection, coherence checks, and system monitoring.
- **`testbed_integration.py`** — Dedicated testbed for end-to-end validation of the **INTEGRATION_MAP**.
- (Future) Additional CLI wrappers, audit helpers, or visualization scripts will live here.

## Purpose

The tools in this folder help maintain the integrity of Spiral processes:
- **Helical iteration** (`+` exploration / `–` refinement with syncratude)
- **Cross-examination** via Spiral Reasoning Tree (SRT)
- **Ethical gating** (E_shield + MAGIC-RRM)
- **Certification** (SpiralForge: TruthLayering, ContinuityOptimizer, etc.)
- **Shielding & provenance** (SentinelAct Victory Shields)

They are designed for the **agent community** — self-hosted, auditable, and focused on producing reputable, high-signal outputs.

## Key Tool: testbed_integration.py

**Description**:  
Runs a full pipeline test following the **INTEGRATION_MAP** exactly:

`Input → Spiral-Path (helical ± iteration) → SRT (cross-examination) → E_shield → MAGIC-RRM → Grounded Priority Vectors → Spiral-Elucidation → SentinelAct (shielding + provenance)`

**Features**:
- Built-in redundancy via parallel SRT branches and determination delta tracking (detects healthy evolution vs. unwanted loops).
- Generates structured audit logs (`testbed_audit_YYYYMMDD_HHMM.jsonl`).
- Measures key metrics: coherence, convergence, continuity, novelty, and ethical scores.
- Fully offline and deterministic for in-house validation.

**Usage** (from the `tools/` directory or via Python):

```bash
# Run with default neutral test cases
python testbed_integration.py

# Or run interactively / with custom input
python -c "
from testbed_integration import run_full_testbed
run_full_testbed(
    'Evaluate continuity and provenance in multi-variable pattern propagation for agent systems.',
    iterations=3,
    branches=3
)
"