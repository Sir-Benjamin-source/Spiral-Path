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

st.markdown("---")
st.write("Built with Spiral Theory—fork on GitHub, cite via Zenodo DOI: [10.5281/zenodo.16585562](https://doi.org/10.5281/zenodo.16585562). Ethical AI: Human seal encouraged.")
