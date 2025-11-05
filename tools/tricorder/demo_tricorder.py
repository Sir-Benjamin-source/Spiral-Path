import streamlit as st
import sys
import os

# Robust path hack: Append current and parent dirs
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, '..'))  # Parent for package

try:
    from core import tricorder_scan  # Relative fallback if in dir
    from ais import ais_scan
except ImportError:
    try:
        from tricorder.core import tricorder_scan  # Absolute if package
        from tricorder.ais import ais_scan
    except ImportError as e:
        st.error(f"Import error: {e}. Ensure core.py and ais.py in tricorder/. Run from /tools/ or install with setup.py.")
        st.stop()

import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import networkx as nx

st.title("Spiral Path Tricorder Demo")
st.write("Probe contexts with Spiral eq + SRM ethics. AIS mode for quant.")

seed = st.text_input("Context Seed", value="debug latency")
domain = st.selectbox("Domain", ["tech", "poetic", "research"])
max_iters = st.slider("Max Iters", 1, 10, 3)
td_max = st.slider("Tangent Depth", 1, 5, 3)
ais_mode = st.checkbox("Enable AIS (ethics + quant)")

if st.button("Scan"):
    try:
        if ais_mode:
            result = ais_scan(seed, domain, max_iters)
            st.subheader("AIS Results")
            st.metric("Consent Factor", f"{result.get('consent_factor', 1.0):.2f}")
            st.metric("Pruned Tangents", result['srm'].get('pruned_tangents', 0))
            csv_buffer = BytesIO()
            pd.DataFrame([result]).to_csv(csv_buffer, index=False)
            st.download_button("Download Quant CSV", csv_buffer.getvalue(), "tricorder_quant.csv")
        else:
            result = tricorder_scan(seed, domain, max_iters, td_max)
            st.subheader("Standard Results")
        
        st.write("### Chains")
        df_primary = pd.DataFrame(result['chains']['primary_chain'], columns=['Source', 'Target', 'Weight'])
        st.dataframe(df_primary)
        
        st.write("### Alt Fork")
        df_fork = pd.DataFrame(result['chains']['poetic_fork'])
        st.dataframe(df_fork)
        
        st.metric("Hypothesis Strength", f"{result['chains']['hypothesis_strength']:.2f}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ethics Drift", f"{result['srm']['ethics_drift']:.2f}")
        with col2:
            st.metric("Fire Integrity", f"{result['srm']['fire_integrity']:.2f}")
        
        # Viz
        fig, ax = plt.subplots(figsize=(8, 6))
        G = nx.DiGraph()
        for edge in result['chains']['primary_chain']:
            G.add_edge(edge[0], edge[1], weight=edge[2])
        nx.draw(G, with_labels=True, ax=ax, node_color='lightblue')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Scan error: {e}. Check deps (pandas, networkx, matplotlib).")

st.write("---")
st.caption("Powered by Spiral Theory & A.I.S. Standards. DOI pending.")
