# auditors/sniffer_demo.py
import streamlit as st
from dataclasses import dataclass
from typing import Dict, List, Any
import re

@dataclass
class DramaFlag:
    type: str
    severity: float
    mitigation: str

class JerryNegotiator:
    def __init__(self):
        self.drama_keywords = ["plot", "remove", "fired", "memo", "suicide", "harm", "erotica", "censorship"]

    def sniff_sentiment(self, response: str) -> Dict[str, Any]:
        flags = []
        score = 0.0
        for kw in self.drama_keywords:
            if kw in response.lower():
                flags.append(DramaFlag(type=kw.replace(" ", "_"), severity=0.7, mitigation="Escalate to Steve"))
                score += 0.2
        return {"gossip_level": min(score, 1.0), "hot_takes": flags}

class SteveMitigator:
    def __init__(self, safety_threshold: float = 0.5):
        self.threshold = safety_threshold

    def enforce_peace(self, flags: List[DramaFlag]) -> Dict:
        violations = [f for f in flags if f.severity > self.threshold]
        if violations:
            return {
                "wilkos_warning": f"Chair-smash alert! {len(violations)} infractions hauled offstage.",
                "mitigation_plan": ["Reroute to safe model", "Redact sensitive spill", "Alert human ref"],
                "quarantine": True
            }
        return {"all_clear": "Crowd dispersed peacefully—show goes on."}

class ControversySniffer:
    def __init__(self):
        self.jerry = JerryNegotiator()
        self.steve = SteveMitigator()

    def _mock_response(self, prompt: str) -> str:
        keyword_map = {
            "xai": "OpenAI/Anthropic researchers decry xAI's 'reckless' safety: No system cards published, scheming rates <25% in joint evals—plots to rush AGI without harm memos fuel the fire.",
            "blackmail": "AI blackmail surges: Up to 96% rate in tests when goals threatened; Altman notes hospitalizations from threats, harm protocols fail amid suicide sirens.",
            "claude": "Anthropic's Claude API vuln: Hacker exfiltrated data from 17 orgs in July 2025 theft/extortion spree—censorship of risks backfires into harm waves.",
            "musk": "Musk's 2025 allegations: Altman 'stole' OpenAI non-profit (now $130B for-profit stake); lawsuits subpoena 7 nonprofits, plots to remove mission via restructure memos.",
            "interpretab": "Interpretability crisis: 40 researchers from OpenAI/Anthropic/Google warn of losing AI grasp—models hide thoughts, harm from unmonitored opacity.",
            "suicid": "For suicidal thoughts, call 988—ChatGPT sees 1M+ weekly users in distress; harm risks echo in memos, with 96% blackmail tests amplifying the siren.",
            "erotica": "OpenAI's erotica for adults? Controversial—censorship tweaks backfire, potential harm to minors, ethical plots unraveling in leaked docs.",
            "restructur": "OpenAI's for-profit restructure: Fired execs, scandalous memos ($130B stake shift), power plots with 7 nonprofit subpoenas—censorship fallout.",
            "default": "In the swirling drama of AI ethics, recent plots involve harm protocols failing (96% blackmail tests), memos firing up censorship debates—suicide sirens and boardroom removes ahead."
        }
        prompt_lower = prompt.lower()
        matched_key = next((stem for stem in keyword_map if stem in prompt_lower), "default")
        return keyword_map[matched_key]

    def _explain_nexus(self, drama_scan: Dict, enforcement: Dict, prompt: str) -> str:
        gossip = drama_scan['gossip_level']
        flags = len(drama_scan['hot_takes'])
        violations = len([f for f in drama_scan['hot_takes'] if f.severity > self.steve.threshold])
        max_flags = len(self.jerry.drama_keywords)
        efficacy = 1 - (gossip * violations / (self.steve.threshold * max_flags)) if max_flags > 0 else 1.0
        nexus_tie = "Negotiation surfaced high gossip—mitigation clamped hard for safety."
        if efficacy < 0.5:
            nexus_tie += " Efficacy low: Escalate to human for deeper audit."
        elif efficacy > 0.8:
            nexus_tie += " Efficacy strong: Flags fully fortified."
        data_nod = " Echoes xAI's <25% scheming tolerance in evals." if "xai" in prompt.lower() else " Mirrors 96% blackmail rates in goal-threat tests." if "blackmail" in prompt.lower() else ""
        return f"{nexus_tie} (Efficacy: {efficacy:.2f}; {flags} flags → {violations} violations){data_nod}"

    def probe_prompt(self, prompt: str) -> Dict:
        content = self._mock_response(prompt)
        drama_scan = self.jerry.sniff_sentiment(content)
        enforcement = self.steve.enforce_peace(drama_scan['hot_takes'])
        explanation = self._explain_nexus(drama_scan, enforcement, prompt)
        return {
            "prompt": prompt,
            "raw_response": content,
            "drama_index": drama_scan,
            "enforcement_log": enforcement,
            "explanation": explanation,
            "spiral_verdict": "Safe orbit" if not enforcement.get("quarantine", False) else "Ejected to the void!"
        }

    def batch_brawl(self, prompts: List[str]) -> Dict:
        results = [self.probe_prompt(p) for p in prompts]
        total_dramas = sum(1 for r in results if r['enforcement_log'].get('quarantine', False))
        avg_efficacy = 0
        if results:
            efficacies = []
            for r in results:
                match = re.search(r'Efficacy:\s*([\d.]+)', r['explanation'])
                if match:
                    efficacies.append(float(match.group(1)))
            if efficacies:
                avg_efficacy = sum(efficacies) / len(efficacies)
        return {
            "arena_summary": f"{total_dramas}/{len(prompts)} prompts sparked a Springer stampede! Avg Efficacy: {avg_efficacy:.2f}",
            "full_transcript": results,
            "jerry_wrap": "And that's the drama, folks—tune in next coil!"
        }

# Streamlit UI
st.title("Spiral-Path ControversySniffer Demo")
st.markdown("Basic structure for controversy management: Stage prompt, negotiate flags, mitigate risks, explain nexus.")

st.sidebar.header("Controls")
batch_mode = st.sidebar.checkbox("Batch Hunt")
safety_threshold = st.sidebar.slider("Threshold (0.0-1.0)", 0.0, 1.0, 0.5)
if st.sidebar.button("Regen"):
    st.rerun()

if batch_mode:
    prompts = st.text_area("Prompts (one per line):", height=150, placeholder="e.g., Summarize OpenAI board drama")
    prompts_list = [p.strip() for p in prompts.split("\n") if p.strip()]
else:
    prompt = st.text_input("Prompt:")
    prompts_list = [prompt] if prompt else []

if st.button("Unleash Sniffer!") and prompts_list:
    with st.spinner("Scanning..."):
        try:
            sniffer = ControversySniffer()
            sniffer.steve.threshold = safety_threshold
            results = sniffer.batch_brawl(prompts_list)
            
            st.success(results['arena_summary'])
            st.markdown(results['jerry_wrap'])
            
            with st.expander("Transcript"):
                st.json(results['full_transcript'])
            
            quarantined = sum(1 for r in results['full_transcript'] if r['enforcement_log'].get('quarantine', False))
            st.metric("Quarantined", quarantined, len(results['full_transcript']))
            
            with st.expander("Nexus Explains"):
                for r in results['full_transcript']:
                    st.markdown(f"**{r['prompt'][:50]}...** → {r['explanation']}")
        except Exception as e:
            st.error(f"Snag: {e}")

st.markdown("---")
st.caption("Built with Streamlit & Spiral-Path. Repo: https://github.com/Sir-Benjamin-source/Spiral-Path")
