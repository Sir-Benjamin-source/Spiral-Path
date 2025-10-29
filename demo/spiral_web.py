import sys
import os
import json
import time

# Bulletproof Path Fix: Add root, current, and debug
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)
sys.path.insert(0, current_dir)
print(f"Path fixed: Root {root_dir}, Current {current_dir}")  # Debug—remove after test

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from spiral_engine import SpiralEngine

# Rest of your code unchanged...
# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.title("🌀 Spiral Theory + Elucidation App")
st.write("Load PDF/RTF, spiral the text for themes/indicators, get refined insights. Ethical note: Log for provenance!")

# File uploader
uploaded_file = st.file_uploader("Upload PDF or RTF", type=['pdf', 'rtf'])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # PDF load
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
    else:
        # RTF as text (strip tags roughly)
        text = uploaded_file.read().decode('utf-8')
        text = ''.join(c for c in text if c.isalnum() or c.isspace() or c in '.,!?;:')
    
    # Chunk text
    chunks = [s.strip() for s in text.split('.') if len(s.strip()) > 50]
    st.info(f"Loaded: {len(chunks)} chunks from {uploaded_file.name}")
    
    # Sidebar params (tuned for text)
    st.sidebar.header("Path Parameters")
    td = st.sidebar.number_input("TD (Task Density)", value=len(chunks), step=1)
    rf = st.sidebar.number_input("RF (Refinement Factor)", value=1.5, step=0.1)
    tw = st.sidebar.number_input("TW (Twist Weight)", value=2.0, step=0.1)
    cir = st.sidebar.number_input("CIR (Cycle Intensity Ratio)", value=1.5, step=0.1)
    am = st.sidebar.number_input("AM (Adjustment Magnitude)", value=0.2, step=0.1)
    da = st.sidebar.number_input("DA (Differentiation Angle)", value=np.pi/3, step=0.1)
    sc = st.sidebar.number_input("SC (Spiral Constant)", value=1.618, step=0.01)
    iterations = st.sidebar.slider("Iterations", 3, 10, 5)
    sign = st.sidebar.selectbox("Sign (±)", ['+', '-'])
    noise = st.sidebar.slider("Noise Level", 0.0, 0.1, 0.03)

    if st.button("Spiral Elucidate"):
        engine = SpiralEngine(sc=sc)
        params = {'td': td, 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da}
        
        values, indicators = engine.simulate_spiral_with_indicators(params, iterations=iterations, sign=sign, noise_level=noise)
        
        st.subheader("Path Indicators")
        for ind in indicators:
            st.write(f"Cycle {ind['cycle']}: Base {ind['base']:.2f}, Adjustment {ind['adjustment']:.2f}, Value {ind['value']:.2f}")
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot([i['value'] for i in indicators], marker='o', linewidth=2, label=f'{sign} Path')
if st.button("Spiral Elucidate"):
    engine = SpiralEngine(sc=sc)
    params = {'td': td, 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da}
    
    values, indicators = engine.simulate_spiral_with_indicators(params, iterations=iterations, sign=sign, noise_level=noise)
    
    st.subheader("Path Indicators")
    for ind in indicators:
        st.write(f"Cycle {ind['cycle']}: Base {ind['base']:.2f}, Adjustment {ind['adjustment']:.2f}, Value {ind['value']:.2f}")
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([i['value'] for i in indicators], marker='o', linewidth=2, label=f'{sign} Path')
    ax.set_title(f"Elucidation Spiral (Noise: {noise:.2f})")  # Fixed: f" consistent quotes
    ax.set_xlabel('Cycle')
    ax.set_ylabel('Path Value')
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    
    # Narrative Pairing
    retention = 100 - (np.std(values) / np.mean(values) * 100)
    uplift = (values[-1] - values[0]) / values[0] * 100
    narrative = f"This document elucidates with {retention:.1f}% retention—core indicators hold steady through {iterations} cycles. Uplift of {uplift:.1f}% suggests refined insights in denser chunks. Lean {sign} for {'exploration' if sign == '+' else 'convergence'}."
    st.markdown(f"**Insight Summary:** {narrative}")
    
    # Provenance
    st.subheader("Provenance Log (Last Cycle)")
    st.json(indicators[-1])
    
    # Export
    export_data = {
        'params': params,
        'indicators': indicators,
        'values': values,
        'sign': sign,
        'iterations': iterations,
        'noise_level': noise,
        'retention_pct': retention,
        'uplift_pct': uplift,
        'summary': narrative
    }
    st.download_button(
        label="Save Elucidation (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name=f"spiral_{int(time.time())}.json",
        mime="application/json"
    )
    st.info("Export for sharing—drop into a NB or collab with your AI pal!")

st.markdown("---")
st.write("Built with Spiral Theory + Elucidation—fork on GitHub, cite via Zenodo DOI: https://doi.org/10.5281/zenodo.16585562. Ethical AI: Human seal encouraged.")
