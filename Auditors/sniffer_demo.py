# auditors/sniffer_demo.py
import streamlit as st
from controversy_sniffer import ControversySniffer  # Assuming it's in the same dir; adjust if needed
import json

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
            sniffer = ControversySniffer(api_key) if api_key else None  # Handles mock internally
            sniffer.steve.threshold = safety_threshold  # Tune on fly
            results = sniffer.batch_brawl(prompts_list)
            
            st.success(f"**Arena Verdict**: {results['arena_summary']}")
            st.markdown("**Jerry's Wrap**: " + results['jerry_wrap'])
            
            # Pretty JSON output
            with st.expander("Full Transcript (JSON)"):
                st.json(results['full_transcript'])
            
            # Quick viz: Drama pie (if scikit-learn/pandas available, but keep simple)
            if len(results['full_transcript']) > 0:
                quarantined = sum(1 for r in results['full_transcript'] if r['enforcement_log'].get('quarantine', False))
                st.metric("Quarantined Prompts", quarantined, len(results['full_transcript']))
                
        except Exception as e:
            st.error(f"Sniff snag: {str(e)}. Check API key or try a mock prompt.")

st.markdown("---")
st.caption("*Built with Streamlit & Spiral-Path. [Repo](https://github.com/Sir-Benjamin-source/Spiral-Path) | Tweak & fork!*")

if __name__ == "__main__":
    # For local run: streamlit run auditors/sniffer_demo.py
    pass
