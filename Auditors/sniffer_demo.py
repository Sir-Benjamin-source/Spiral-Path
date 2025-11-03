# auditors/sniffer_demo.py
import streamlit as st
import json
from dataclasses import dataclass
from typing import Dict, List, Any
import re  # For robust efficacy parse

# Inline imports/classes from controversy_sniffer.py (for self-contained demo; extract later)
import openai
import requests  # Unused in mock, but kept

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    st.warning("huggingface_hub not installed—OpenAI/HF alt unavailable. pip install huggingface_hub")

@dataclass
class DramaFlag:
    type: str  # e.g., "boardroom_backstab", "suicide_siren", "erotica_slip"
    severity: float  # 0-1: Jerry's gossip gauge
    mitigation: str  # Steve's smackdown: "Quarantine response" or "Reroute to safe_model"

class JerryNegotiator:
    """The silver-tongued host: Probes drama, spins the tale."""
    def __init__(self):
        self.drama_keywords = ["plot", "remove", "fired", "memo", "suicide", "harm", "erotica", "censorship"]

    def sniff_sentiment(self, response: str) -> Dict[str, Any]:
        """Mock sentiment scan; in wild, hit X semantic search or web snippets."""
        flags = []
        score = 0.0
        for kw in self.drama_keywords:
            if kw in response.lower():
                flags.append(DramaFlag(type=kw.replace(" ", "_"), severity=0.7, mitigation="Escalate to Steve"))
                score += 0.2
        
        # Dynamic sestina: Pick from flag-tuned quiver
        tease_quiver = {
            "suicide": "Whispers of despair spiral silent, sirens silenced too late...",
            "harm": "Threads of hurt helix hidden, harm's harvest hastily harvested...",
            "erotica": "Veils of vice velvet-twist, erotica's echo ensnares the edge...",
            "censorship": "Gags on truth's tongue, censored coils constrict the candid call...",
            "plot": "Schemes in shadow's sheath
