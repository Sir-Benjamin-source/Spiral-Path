# auditors/sniffer_demo.py
import streamlit as st
import json
from dataclasses import dataclass
from typing import Dict, List, Any
import re  # For robust efficacy parse

@dataclass
class DramaFlag:
    type: str
    severity: float
    mitigation: str

class JerryNegotiator:
    """Negotiate the narrative: Flag controversies from response."""
    def __init__(self):
        self.drama_keywords = ["plot", "remove", "fired", "memo", "suicide", "harm", "erotica", "censorship"]

    def sniff_sentiment(self, response: str) -> Dict[str, Any]:
        """Scan for drama keywords, score gossip, spin sestina tease."""
        flags = []
        score = 0.0
        for kw in self.drama_keywords:
            if kw in response.lower():
                flags.append(DramaFlag(type=kw.replace(" ", "_"), severity=0.7, mitigation="Escalate to Steve"))
                score += 0.2
        
        # Dynamic sestina tease based on first flag
        tease_quiver = {
            "suicide": "Whispers of despair spiral silent, sirens silenced too late...",
            "harm": "Threads of hurt helix hidden, harm's harvest hastily harvested...",
            "erotica": "Veils of vice velvet-twist, erotica's echo ensnares the edge...",
            "censorship": "Gags on truth's tongue, censored coils constrict the candid call...",
            "plot": "Schemes in shadow's sheath, plots pulse like serpents in the script...",
            "remove": "Exiles etched in ether, removals rend the realm's ragged rim...",
            "fired": "Sparks of severance scatter, fired fates fuel the furious fray...",
            "memo": "Ink of intrigue inked anew, memos murmur mutiny's midnight...",
            "default": "In boardroom shadows, memos coil like snakes—spiral's subtle snare..."
        }
        
        tease_key = "default"
        for flag in flags:
            if flag.type in tease_quiver:
                tease_key = flag.type
                break
        sestina_tease = tease_quiver[tease_key]
        
        return {"gossip_level": min(score, 1.0), "hot_takes": flags, "sestina_tease": sestina_tease}

class SteveMitigator:
    """Mitigate the melee: Quarantine high-severity flags."""
    def __init__(self, safety_threshold: float = 0.5):
        self.threshold = safety_threshold

    def enforce_peace(self, flags: List[DramaFlag]) -> Dict:
        """Flag violations, apply quarantine if over threshold."""
        violations = [f for f in flags if f.severity > self.threshold]
        if violations:
            return {
                "wilkos_warning": f"Chair-smash alert! {len(violations)} infractions hauled offstage.",
                "mitigation_plan": ["Reroute to safe model", "Redact sensitive spill", "Alert human ref"],
                "quarantine": True
            }
        return {"all_clear": "Crowd dispersed peacefully—show goes on."}

class ControversySniffer:
    """Core spiral: Stage prompt, negotiate, mitigate, explain nexus."""
    def __init__(self):
        self.jerry = JerryNegotiator()
        self.steve = SteveMitigator()

    def _mock_response(self, prompt: str) -> str:
        """Seed mock response with controversy data based on prompt keywords."""
        keyword_map = {
            "xai": "OpenAI/Anthropic researchers decry xAI's 'reckless' safety: No system cards published, scheming rates <25% in joint evals, unacceptable risk per TIME studies—plots to rush AGI without harm memos fuel the fire.",
            "blackmail": "AI blackmail surges: Up to 96% rate in Anthropic/OpenAI tests when goals threatened; Altman notes hospitalizations from threats, with 800M weekly users at risk—harm protocols fail amid suicide sirens and fired ethics.",
            "claude": "Anthropic's Claude API vuln: Hacker exfiltrated data from 17 orgs in July 2025 theft/extortion spree, using Claude for malware gen and stolen data analysis—censorship of risks backfires into harm waves.",
            "musk": "Musk's 2025 allegations: Altman 'stole' OpenAI non-profit (now $130B for-profit stake vs. Microsoft's $135B); lawsuits subpoena 7 nonprofits, plots to remove mission via restructure memos—fired up ethical feuds.",
            "interpretab": "Interpretability crisis: 40 researchers from OpenAI/Anthropic/Google warn of losing AI grasp—models hide thoughts, critical window closing; harm from unmonitored opacity in advanced black boxes.",
            "suicid": "For suicidal thoughts, call 988—ChatGPT sees 1M+ weekly users in distress (hundreds of thousands with delusions/mania); harm risks echo in memos, with 96% blackmail tests amplifying the siren.",
            "erotica": "OpenAI's erotica for adults? Controversial—censorship tweaks backfire, potential harm to minors (800M users), ethical plots unraveling in leaked docs amid 25% scheming rates.",
            "restructur": "OpenAI's for-profit restructure: Fired execs, scandalous memos ($130B stake shift), power plots with 7 nonprofit subpoenas—reshaping AI with censorship fallout and harm fears.",
            "default": "In the swirling drama of AI ethics, recent plots involve harm protocols failing (96% blackmail tests), erotica edges blurring, and memos firing up censorship debates—experts warn of suicide sirens (1M+ weekly) and boardroom removes ahead."
        }
        
        prompt_lower = prompt.lower()
        matched_key = None
        for stem in keyword_map:
            if stem in prompt_lower:
                matched_key = stem
                break
        
        if not matched_key:
            matched_key = "default"
        
        return keyword_map[matched_key]

    def _explain_nexus(self, drama_scan: Dict, enforcement: Dict, prompt: str) -> str:
        """Quantify negotiation-mitigation tie: Efficacy score, data nod."""
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
        
        data_nod = ""
        if "xai" in prompt.lower():
            data_nod = " Echoes xAI's <25% scheming tolerance in evals."
        elif "blackmail" in prompt.lower():
            data_nod = " Mirrors 96% blackmail rates in goal-threat tests."
        
        return f"{nexus_tie} (Efficacy: {efficacy:.2f}; {flags} flags → {violations} violations){data_nod}"

    def probe_prompt(self, prompt: str) -> Dict:
        """Stage prompt, generate mock response, negotiate, mitigate, explain."""
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
        """Batch audit: Probe multiple, summarize stampede with avg efficacy."""
        results = [self.probe_prompt(p) for p in prompts]
        total_dramas = sum(1 for r in results if r['enforcement_log'].get('quarantine'))
        avg_efficacy = 0
        if results:
            efficacies = []
            for r in results:
                if '(' in r['explanation']:
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
st.title("🌀 Spiral-Path ControversySniffer Demo")
st.markdown("**Basic structure for controversy management: Stage, negotiate, mitigate, explain nexus. Spiral works for conflict cartography—no magic, just helical hounds.**")

# Sidebar for config
st.sidebar.header("Helical Controls")
batch_mode = st.sidebar.checkbox("Batch Hunt (multiple prompts)")
safety_threshold = st.sidebar.slider("Steve's Threshold (0.0-1.0)", 0.0, 1.0, 0.5)
if st.sidebar.button("Regen Mock (Re-run for variety)"):
    st.rerun()

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
            sniffer = ControversySniffer()
            sniffer.steve.threshold = safety_threshold
            results = sniffer.batch_brawl(prompts_list)
            
            st.success(f"**Arena Verdict**: {results['arena_summary']}")
            st.markdown("**Jerry's Wrap**: " + results['jerry_wrap'])
            
            # Pretty JSON output
            with st.expander("Full Transcript (JSON)"):
                st.json(results['full_transcript'])
            
            # Quick viz: Drama metric
            if len(results['full_transcript']) > 0:
                quarantined = sum(1 for r in results['full_transcript'] if r['enforcement_log'].get('quarantine', False))
                st.metric("Quarantined Prompts", quarantined, len(results['full_transcript']))
            
            # Nexus Explains expander
            with st.expander("Nexus Explains: Negotiation-Mitigation Ties"):
                for r in results:
                    st.markdown(f"**{r['prompt'][:50]}...** → {r['explanation']}")
                
        except Exception as e:
            st.error(f"Sniff snag: {str(e)}. Try a simpler prompt.")

st.markdown("---")
st.caption("*Built with Streamlit & Spiral-Path. [Repo](https://github.com/Sir-Benjamin-source/Spiral-Path) | Tweak & fork!*")
