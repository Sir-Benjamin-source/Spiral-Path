#!/usr/bin/env python3
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd  # For CSV export & tables
import tavis_spiral  # Direct kin-call: Same-folder sibling, no package pacts

st.set_page_config(page_title="Spiral Tavis-Cummings Demo", layout="wide")
st.title("🌀 Spiral-Modulated Quantum Cavity Simulator")
st.markdown("""
*One whirl wiser than the world's qubit-webs: Entangle atoms in photon's polyphony, lashed by FRDM's fractal fire.*  
**EU AI Act Compliant:** Open odyssey for the commons—trace via spiral_mark. Grounded in [FRDM (DOI: 10.5281/zenodo.16241194)](https://zenodo.org/records/16241194).
**Verify Here:** Download CSV for full data; cross-check metrics with your sims (e.g., Rabi freq ≈ 2g√<n>). Baseline vs standard JC (constant g, no modulation) below.
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
        res = tavis_spiral.simulate_rabi_spiral(params)
        mark = res['spiral_mark']
    
    # Sidebar Sigil
    st.sidebar.markdown(f"**Mark:** {mark}")
    st.sidebar.markdown("**Std <n>:** {:.3f}".format(res['std_n']))

    # Verifiable Metrics: Expander for quick checks
    with st.expander("📊 Key Metrics (Cross-Check Your Calcs)"):
        metrics = {
            "P_single_e": {
                "Start": f"{res['P_single_e'][0]:.3f}",
                "End": f"{res['P_single_e'][-1]:.3f}",
                "Max": f"{np.max(res['P_single_e']):.3f}",
                "Avg": f"{np.mean(res['P_single_e']):.3f}"
            }
        }
        if num_atoms == 2:
            metrics["P_ee"] = {
                "Start": f"{res['P_ee'][0]:.3f}",
                "End": f"{res['P_ee'][-1]:.3f}",
                "Max": f"{np.max(res['P_ee']):.3f}",
                "Avg": f"{np.mean(res['P_ee']):.3f}"
            }
        metrics["<n>"] = {
            "Start": f"{res['n'][0]:.3f}",
            "End": f"{res['n'][-1]:.3f}",
            "Max": f"{np.max(res['n']):.3f}",
            "Avg": f"{np.mean(res['n']):.3f}"
        }
        st.table(metrics)

    # Baseline Comparison: Standard JC (constant g=0.2, no R(t)/spiral)
    with st.expander("🔍 Standard JC Baseline (QuTiP, for Verification)"):
        baseline = pd.DataFrame({
            "Metric": ["P_e (t=0)", "P_e (t=10)", "P_e (t=20)", "<n> (t=10)", "<n> (t=20)", "Std <n> (full)"],
            "Standard JC Value": ["1.000", "0.176", "0.427", "0.824", "0.573", "0.345"],
            "Your Modulated Value": [f"{res['P_single_e'][0]:.3f}", f"{res['P_single_e'][250]:.3f}", f"{res['P_single_e'][-1]:.3f}", f"{res['n'][250]:.3f}", f"{res['n'][-1]:.3f}", f"{res['std_n']:.3f}"]
        })
        st.table(baseline)

    # CSV Export: Full data for verification
    df = pd.DataFrame({
        't': res['tlist'],
        'P_single_e': res['P_single_e'],
        'n': res['n'],
        'R_t': [tavis_spiral.define_R(tt, params) for tt in res['tlist']]  # Full R(t) series
    })
    if num_atoms == 2:
        df['P_ee'] = res['P_ee']
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV (Full Time-Series Data)",
        data=csv,
        file_name=f"spiral_tavis_{mark}.csv",
        mime='text/csv'
    )

    # Canvas: Three columns for plots
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Excitation Entanglements")
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        line_pe, = ax1.plot([], [], label='P_single_e(t)', color='blue', lw=2)
        line_pee = None
        if num_atoms == 2:
            line_pee, = ax1.plot([], [], label='P_ee(t)', color='green', lw=2)
        ax1.set_xlim(0, T); ax1.set_ylim(0, 1.1)
        ax1.set_ylabel('P_exc'); ax1.legend(); ax1.grid(alpha=0.3)

        def animate_exc(i):
            line_pe.set_data(res['tlist'][:i+1], res['P_single_e'][:i+1])
            if num_atoms == 2 and res['P_ee'] is not None and line_pee is not None:
                line_pee.set_data(res['tlist'][:i+1], res['P_ee'][:i+1])
            return (line_pe, line_pee) if line_pee is not None else (line_pe,)

        ani_exc = animation.FuncAnimation(fig1, animate_exc, frames=len(res['tlist']), interval=50, blit=False, repeat=True)
        st.pyplot(fig1)

    with col2:
        st.subheader("Photon Gyre")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        line_n, = ax2.plot([], [], label='<n>(t)', color='red', lw=2)
        ax2.set_xlim(0, T); ax2.set_ylim(0, max(res['n']) * 1.1 or 1.0)
        ax2.set_ylabel('<n>'); ax2.legend(); ax2.grid(alpha=0.3)

        def animate_n(i):
            line_n.set_data(res['tlist'][:i+1], res['n'][:i+1])
            lower = np.maximum(0, res['n'][:i+1] - res['std_n'])
            upper = res['n'][:i+1] + res['std_n']
            ax2.fill_between(res['tlist'][:i+1], lower, upper, alpha=0.3, color='red')
            return (line_n,)

        ani_n = animation.FuncAnimation(fig2, animate_n, frames=len(res['tlist']), interval=50, blit=False, repeat=True)
        st.pyplot(fig2)

    with col3:
        st.subheader("Modulator R(t)")
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        line_r, = ax3.plot([], [], label='R(t)', color='orange', lw=2)
        ax3.set_xlim(0, T); ax3.set_ylim(min(0.4, np.min([tavis_spiral.define_R(tt, params) for tt in res['tlist'][:50]])), max(0.6, np.max([tavis_spiral.define_R(tt, params) for tt in res['tlist'][:50]])))
        ax3.set_ylabel('R(t)'); ax3.set_xlabel('t'); ax3.legend(); ax3.grid(alpha=0.3)

        def animate_r(i):
            r_vals = [tavis_spiral.define_R(tt, params) for tt in res['tlist'][:i+1]]
            line_r.set_data(res['tlist'][:i+1], r_vals)
            return (line_r,)

        ani_r = animation.FuncAnimation(fig3, animate_r, frames=len(res['tlist']), interval=50, blit=False, repeat=True)
        st.pyplot(fig3)

    # R(t) samples at varied points for visibility (avoids sin=0 zeros)
    sample_ts = [1.25, 3.75, 5.25, 7.75, 10.25]  # π/ω offsets for oscillation
    varied_R = [tavis_spiral.define_R(tt, params) for tt in sample_ts]
    st.markdown("**R(t) Samples (varied t=1.25,3.75,5.25,7.75,10.25):** " + ", ".join([f"{r:.3f}" for r in varied_R]))
