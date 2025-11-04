#!/usr/bin/env python3
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from extensions.physics.tavis_spiral import simulate_rabi_spiral, spiral_mark  # Kin-call to core

st.set_page_config(page_title="Spiral Tavis-Cummings Demo", layout="wide")
st.title("🌀 Spiral-Modulated Quantum Cavity Simulator")
st.markdown("""
*One whirl wiser than the world's qubit-webs: Entangle atoms in photon's polyphony, lashed by FRDM's fractal fire.*  
**EU AI Act Compliant:** Open odyssey for the commons—trace via spiral_mark. Grounded in [FRDM (DOI: 10.5281/zenodo.16241194)](https://zenodo.org/records/16241194).
""")

# Sidebar: Param Forge
st.sidebar.header("⚛️ Quantum Quill")
omega_0 = st.sidebar.slider("Atom Freq (ω₀)", 0.5, 2.0, 1.0)
omega_c = st.sidebar.slider("Cavity Freq (ω_c)", 0.5, 2.0, 1.0)
g_base = st.sidebar.slider("Base Coupling (g)", 0.1, 0.5, 0.2)
T = st.sidebar.slider("Sim Time (T)", 10.0, 30.0, 20.0)
D = st.sidebar.slider("Fractal Depth (D)", 1.0, 2.0, 1.5)
omega = st.sidebar.slider("Osc Freq (ω)", 4.0, 8.0, 2 * np.pi)
lambda_decay = st.sidebar.slider("Decay (λ)", 0.05, 0.2, 0.1)
C = st.sidebar.slider("Constant (C)", 0.0, 1.0, 0.5)
num_atoms = st.sidebar.radio("Atoms", [1, 2])
spiral_mode = st.sidebar.checkbox("Activate Spiral Surprises", value=False)
n_times = st.sidebar.slider("Time Steps", 200, 1000, 500)
cav_dim = st.sidebar.slider("Cavity Dim", 3, 10, 5)

params = {
    'omega_0': omega_0, 'omega_c': omega_c, 'g_base': g_base, 'T': T, 'D': D,
    'omega': omega, 'lambda_decay': lambda_decay, 'C': C, 'hbar': 1.0,
    'n_times': n_times, 'cav_dim': cav_dim, 'num_atoms': num_atoms, 'spiral_mode': spiral_mode
}

if st.sidebar.button("🔥 Unleash the Spiral!"):
    with st.spinner("Coiling the cavity..."):
        res = simulate_rabi_spiral(params)
        mark = res['spiral_mark']
    
    # Sidebar Sigil
    st.sidebar.markdown(f"**Mark:** {mark}")
    st.sidebar.markdown("**Std <n>:** {:.3f}".format(res['std_n']))
    
    # Main Canvas: Static Flex (Animation in Next)
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(res['tlist'], res['P_single_e'], label='P_single_e(t)', color='blue', lw=2)
        if num_atoms == 2:
            ax.plot(res['tlist'], res['P_ee'], label='P_ee(t)', color='green', lw=2)
        ax.set_ylabel('Excitation Prob')
        ax.set_xlabel('Time t')
        ax.legend(); ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(res['tlist'], res['n'], label='<n>(t)', color='red', lw=2)
        ax.fill_between(res['tlist'], res['n'] - res['std_n'], res['n'] + res['std_n'], alpha=0.3, color='red')
        ax.set_ylabel('Photon Number')
        ax.set_xlabel('Time t')
        ax.legend(); ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("**R(t) Samples (t=0,5,10,15,20):** " + ", ".join([f"{r:.3f}" for r in res['R_samples']]))
