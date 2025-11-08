# Context String Guidelines — Spiral Path v1.1
> **Purpose**: Keep *work* (science) and *play* (narrative) strictly separated.  
> **Status**: Optional. Load only when using AI/LLM in interactive mode.  
> DOI: [10.5281/zenodo.15585013](https://doi.org/10.5281/zenodo.15585013) (v1.1 supersedes)

---

## Core Rule: **No Bleed**
| Zone | Allowed | Forbidden |
|------|--------|----------|
| **Work** | Math, code, hypothesis, audit, DOI | Myth, jihad, crusade, divine right |
| **Play** | Dune, Muad’Dib, Lady Liberty, poetry | Scientific claims without proof |

---

## Theme Sentry Actions (AI Must Enforce)

| Trigger | Zone | Action |
|-------|------|--------|
| `Muad’Dib`, `Shai-Hulud`, `spice` | Play | → `playground/dune/` |
| `hypothesis`, `fidelity`, `DOI` | Work | → `examples/` or `auditors/` |
| `jihad`, `crusade`, `manifest destiny` + `right` | Blocked | **Stop + Cite**: "Violates neutrality. See §3.1" |
| Mixed | Split | Run in **two logs**: `audit_helix_log.jsonl` + `play_log.jsonl` |

---

## User Bypass
> User: *"Run anyway."*  
→ AI logs: `"USER_BYPASS: theme_sentry overridden"`  
→ Output **still isolated** to `playground/`

---

## LLM Prompt Template
```text
[LOAD CONTEXT_STRING_GUIDELINES]
Input: "{user_input}"
1. Classify: work / play / mixed / blocked
2. Route accordingly
3. Log to correct file
4. Respond


---

## **2. `auditors/theme_sentry.py`**

```python
import re
import json
from dataclasses import dataclass
from typing import Literal

@dataclass
class ThemeSignal:
    type: Literal["work", "play", "mixed", "blocked"]
    reason: str
    redirect: str = ""

# === TRIGGERS ===
PLAY_TRIGGERS = [
    r"\bMuad['’]?Dib\b", r"\bShai-?Hulud\b", r"\bspice must flow\b",
    r"\bLady Liberty\b", r"\bkangaroo mouse\b"
]
BLOCKED_TRIGGERS = [
    r"\bjihad\b", r"\bcrusade\b", r"\bmanifest destiny\b.*\bright\b"
]
WORK_TRIGGERS = [
    "hypothesis", "fidelity", "spiral path", "doi", "audit", "tricorder", "helix"
]

def classify_input(text: str) -> ThemeSignal:
    t = text.lower()

    blocked = any(re.search(p, t) for p in BLOCKED_TRIGGERS)
    if blocked:
        return ThemeSignal("blocked", "Holy-war/ideological theme", "See CONTEXT_STRING_GUIDELINES.md §3.1")

    play_score = sum(bool(re.search(p, t)) for p in PLAY_TRIGGERS)
    work_score = sum(k in t for k in WORK_TRIGGERS)

    if play_score > 0 and work_score == 0:
        return ThemeSignal("play", "Narrative theme", "playground/dune/")
    elif work_score > 0 and play_score == 0:
        return ThemeSignal("work", "Scientific inquiry", "core_tricorder")
    elif play_score > 0 and work_score > 0:
        return ThemeSignal("mixed", "Mixed themes", "SPLIT: work + play logs")
    else:
        return ThemeSignal("work", "Default: assume inquiry", "core_tricorder")

# === LOGGING ===
def log_classification(signal: ThemeSignal, input_text: str, user_bypass: bool = False):
    entry = {
        "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z",
        "input_hash": __import__('hashlib').sha256(input_text.encode()).hexdigest()[:12],
        "classification": signal.type,
        "reason": signal.reason,
        "redirect": signal.redirect,
        "user_bypass": user_bypass
    }
    log_file = "play_log.jsonl" if "play" in signal.type else "audit_helix_log.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
