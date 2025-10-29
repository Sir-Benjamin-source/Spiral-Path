import sys
import os
import json
import time
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from spiral_engine import SpiralEngine

st.title("🌀 Spiral Theory Path Simulator")
st.write("Tweak params, hit 'Run Spiral,' see the magic unfold. Ethical note: Log your runs for provenance!")

# Sidebar for params
st.sidebar.header("Path Parameters")
td = st.sidebar.number_input("TD (Task Density)", value=10.0, step=0.1, format="%.2f")
rf = st.sidebar.number_input("RF (Refinement Factor)", value=2.0, step=0.1, format="%.2f")
tw = st.sidebar.number_input("TW (Twist Weight)", value=5.0, step=0.1, format="%.2f")
cir = st.sidebar.number_input("CIR (Cycle Intensity Ratio)", value=3.0, step=0.1, format="%.2f")
am = st.sidebar.number_input("AM (Adjustment Magnitude)", value=1.0, step=0.1, format="%.2f")
da = st.sidebar.number_input("DA (Differentiation Angle)", value=2.0, step=0.1, format="%.2f")
sc = st.sidebar.number_input("SC (Spiral Constant)", value=1.618, step=0.01, format="%.3f")
iterations = st.sidebar.slider("Iterations", 3, 10, 5)
sign = st.sidebar.selectbox("Sign (±)", ['+', '-'])
noise = st.sidebar.slider("Noise Level", 0.0, 0.1, 0.05)

if st.button("Run Spiral"):
    engine = SpiralEngine(sc=sc)
    params = {'td': td, 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da}
    
    values = engine.simulate_spiral(params, iterations=iterations, sign=sign, noise_level=noise)
    
    st.subheader("Spiral Values")
    st.write(values)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(values, marker='o', linewidth=2, label=f'{sign} Path')
    ax.set_title(f'Spiral Path Evolution (Noise: {noise:.2f})')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Path Value')
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    
    # Provenance
    st.subheader("Provenance Log (Last Cycle)")
    st.json(engine.get_provenance()[-1])
    
    # Export
    export_data = {
        'params': params,
        'values': values,
        'sign': sign,
        'iterations': iterations,
        'noise_level': noise,
        'provenance': engine.get_provenance()[-1]
    }
    st.download_button(
        label="Save Spiral (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name=f"spiral_{int(time.time())}.json",
        mime="application/json"
    )
    st.info("Export for sharing—drop into a NB or collab with your AI pal!")

st.markdown("---")
st.write("Built with Spiral Theory—fork on GitHub, cite via Zenodo DOI: https://doi.org/10.5281/zenodo.16585562. Ethical AI: Human seal encouraged.")
