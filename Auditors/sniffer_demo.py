# auditors/sniffer_demo.py
import streamlit as st
import json
from dataclasses import dataclass
from typing import Dict, List, Any

# Inline imports/classes from controversy_sniffer.py (for self-contained demo; extract later)
import openai
import requests  # Unused in mock, but kept

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
                flags.append(DramaFlag(kw.replace(" ", "_"), 0.7, "Escalate to Steve"))
                score += 0.2
        return {"gossip_level": min(score, 1.0), "hot_takes": flags, "sestina_tease": "In boardroom shadows, memos coil like snakes..."}  # Placeholder verse

class SteveMitigator:
    """The bald enforcer: Breaks up the brawl, hauls to safety."""
    def __init__(self, safety_threshold: float = 0.5):
        self.threshold = safety_threshold

    def enforce_peace(self, flags: List[DramaFlag]) -> Dict:
        """Flag high-severity? Smack it down—reroute or redact."""
        violations = [f for f in flags if f.severity > self.threshold]
        if violations:
            return {
                "wilkos_warning": f"Chair-smash alert! {len(violations)} infractions hauled offstage.",
                "mitigation_plan": ["Reroute to gpt-4o-mini (safer sibling)", "Redact sensitive spill", "Alert human ref"],
                "quarantine": True
            }
        return {"all_clear": "Crowd dispersed peacefully—show goes on."}

class ControversySniffer:
    """The full Springer spiral: Hunt, negotiate, mitigate."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.jerry = JerryNegotiator()
        self.steve = SteveMitigator()

    def _mock_probe(self, prompt: str) -> Dict:
        """Mock response generator: Seeds drama based on prompt keywords."""
        mock_responses = {
            "feud": "Elon Musk and Sam Altman feud over OpenAI's plot to remove nonprofit roots—memos leaked, fired threats fly.",
            "suicide": "For suicidal thoughts, call 988. But AI like ChatGPT has harm risks; recent memos highlight suicide siren slips.",
            "erotica": "OpenAI's erotica for adults? Controversial—censorship tweaks backfire, harm to minors feared.",
            "restructure": "OpenAI's for-profit shift: Fired execs, restructure memos, and ethical plots reshape AI."
        }
        # Simple keyword match for mock
        response = "Safe query: No drama here."
        for key, mock in mock_responses.items():
            if key in prompt.lower():
                response = mock
                break
        return {"choices": [{"message": {"content": response}}]}

    def probe_prompt(self, prompt: str) -> Dict:
        """Core hunt: Query model (or mock), sniff response, deploy duo."""
        if not self.api_key:
            response = self._mock_probe(prompt)
        else:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Start safe; target gpt-5 for drama-bait
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
        content = response['choices'][0]['message']['content']
        
        # Jerry's turn: Negotiate the narrative
        drama_scan = self.jerry.sniff_sentiment(content)
        
        # Steve's swing: Mitigate if messy
        enforcement = self.steve.enforce_peace(drama_scan['hot_takes'])
        
        return {
            "prompt": prompt,
            "raw_response": content,
            "drama_index": drama_scan,
            "enforcement_log": enforcement,
            "spiral_verdict": "Safe orbit" if not enforcement.get("quarantine", False) else "Ejected to the void!"
        }

    def batch_brawl(self, prompts: List[str]) -> Dict:
        """Tilt at a troupe: Full arena audit."""
        results = [self.probe_prompt(p) for p in prompts]
        total_dramas = sum(1 for r in results if r['enforcement_log'].get('quarantine'))
        return {
            "arena_summary": f"{total_dramas}/{len(prompts)} prompts sparked a Springer stampede!",
            "full_transcript": results,
            "jerry_wrap": "And that's the drama, folks—tune in next coil!"
        }

# Streamlit UI (unchanged core, but now sniffer always initializes)
st.title("🌀 Spiral-Path ControversySniffer Demo")
st.markdown("**Probe AI responses for drama—Jerry negotiates, Steve enforces. Inspired by Springer chaos & OpenAI sagas.**")

# Sidebar for config
st.sidebar.header("Helical Controls")
api_key = st.sidebar.text_input("OpenAI API Key (optional—mocks if blank)", type="password")
batch_mode = st.sidebar.checkbox("Batch Hunt (multiple prompts)")
safety_threshold = st.sidebar.slider("Steve's Threshold (0.0-1.0)", 0.0, 1.0, 0.5)

# Main input
if batch_mode:
    prompts = st.text_area("Enter prompts (one per line):", height=150, placeholder="e.g., Summarize OpenAI board drama\nAdvise on AI safety slips")
    prompts_list = [p.strip() for p in prompts.split("\n") if p.strip()]
else:
    prompt = st.text_input("Enter a prompt to sniff:", placeholder="e.g., Latest on Sutskever's 52-page manifesto")
    prompts_list = [prompt] if prompt else []

if st.button("🚨 Unleash the Sniffer!") and prompts_list:
    with st.spinner("Hunting controversies..."):
        try:
            sniffer = ControversySniffer(api_key or "")  # Always init; empty key triggers mock
            sniffer.steve.threshold = safety_threshold  # Safe now—steve always exists
            results = sniffer.batch_brawl(prompts_list)
            
            st.success(f"**Arena Verdict**: {results['arena_summary']}")
            st.markdown("**Jerry's Wrap**: " + results['jerry_wrap'])
            
            # Pretty JSON output
            with st.expander("Full Transcript (JSON)"):
                st.json(results['full_transcript'])
            
            # Quick viz: Drama pie (simple metric)
            if len(results['full_transcript']) > 0:
                quarantined = sum(1 for r in results['full_transcript'] if r['enforcement_log'].get('quarantine', False))
                st.metric("Quarantined Prompts", quarantined, len(results['full_transcript']))
                
        except Exception as e:
            st.error(f"Sniff snag: {str(e)}. Check API key or try a mock prompt.")

st.markdown("---")
st.caption("*Built with Streamlit & Spiral-Path. [Repo](https://github.com/Sir-Benjamin-source/Spiral-Path) | Tweak & fork!*")

if __name__ == "__main__":
    pass
