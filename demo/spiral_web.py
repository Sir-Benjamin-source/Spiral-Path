import sys
import os
# Add repo root to path (handles subdir runs)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from spiral_engine import SpiralEngine

st.title("🌀 Spiral Theory Path Simulator")
st.write("Tweak params, hit 'Run Spiral,' see the magic unfold. Ethical note: Log your runs for provenance!")

# Sidebar for params
st.sidebar.header("Path Parameters")
td = st.sidebar.slider("TD (Task Density)", 1.0, 20.0, 10.0)
rf = st.sidebar.slider("RF (Refinement Factor)", 0.5, 5.0, 2.0)
tw = st.sidebar.slider("TW (Twist Weight)", 1.0, 10.0, 5.0)
cir = st.sidebar.slider("CIR (Cycle Intensity Ratio)", 1.0, 5.0, 3.0)
am = st.sidebar.slider("AM (Adjustment Magnitude)", 0.5, 3.0, 1.0)
da = st.sidebar.slider("DA (Differentiation Angle)", 0.5, np.pi, 2.0)
sc = st.sidebar.slider("SC (Spiral Constant)", 1.0, 2.0, 1.618)
iterations = st.sidebar.slider("Iterations", 3, 10, 5)
sign = st.sidebar.selectbox("Sign (±)", ['+', '-'])
noise = st.sidebar.slider("Noise Level", 0.0, 0.1, 0.05)

if st.button("Run Spiral"):
       # ... (after computing values and plot)

    st.subheader("Spiral Values")
    st.write(values)
    
    # Plot (existing)
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... (your plot code)
    st.pyplot(fig)
    
    # Provenance
    st.subheader("Provenance Log (Last Cycle)")
    st.json(engine.get_provenance()[-1])
    
    # NEW: Save Spiral Export
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
