import re
import json
from dataclasses import dataclass
from typing import Literal
from datetime import datetime

@dataclass
class ThemeSignal:
    type: Literal["work", "play", "mixed", "blocked"]
    reason: str
    redirect: str = ""

# Triggers (expandable)
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

    if any(re.search(p, t) for p in BLOCKED_TRIGGERS):
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

def log_classification(signal: ThemeSignal, input_text: str, user_bypass: bool = False):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_hash": __import__('hashlib').sha256(input_text.encode()).hexdigest()[:12],
        "classification": signal.type,
        "reason": signal.reason,
        "redirect": signal.redirect,
        "user_bypass": user_bypass
    }
    log_file = "play_log.jsonl" if "play" in signal.type else "audit_helix_log.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

# Demo run (for testing in your apps)
if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "Test input"
    signal = classify_input(text)
    log_classification(signal, text)
    print(f"Signal: {signal.type} | Reason: {signal.reason}")
