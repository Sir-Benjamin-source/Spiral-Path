import sys
import os
import json
import time
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spiral_engine import SpiralEngine

# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.title("🌀 Spiral Theory Path Simulator")
st.write("Tweak params, load a dataset URL, hit 'Analyze Spiral'—watch numbers turn to insights. Ethical note: Log for provenance!")

# Data loader section
st.header("Load Dataset")
url = st.text_input("Paste CSV URL (e.g., Kaggle direct link)")
st.info("💡 For best results (and fewer parsing gremlins), use raw data/document links only—no HTML previews or compressed files. Clean CSVs spiral smoother for us slobs!")
if st.button("Load Data"):
    if url:
        try:
            # Robust read: Loop encodings, seps, quotes, headers
            success = False
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1']:
                for sep in [',', '\t', ';']:
                    for quote in ['"', "'", '']:
                        for header in [0, None]:
                            try:
                                df = pd.read_csv(url, sep=sep, quotechar=quote, encoding=encoding, header=header, on_bad_lines='skip')
                                if df.shape[0] > 0:  # Loaded something
                                    st.session_state.df = df
                                    st.success(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns (enc={encoding}, sep={sep}, header={header}). Columns: {list(df.columns[:5])}...")
                                    with st.expander("Preview First 5 Rows"):
                                        st.dataframe(df.head())
                                    success = True
                                    break
                            except Exception as inner_e:
                                continue
                        if success: break
                    if success: break
                if success: break
            if not success:
                raise ValueError("Tough nut—try a different URL or check for multi-line headers/quotes.")
        except Exception as e:
            st.error(f"Oops—load failed: {e}. Kaggle tip: Export as 'raw CSV' without compression.")
            st.info("Fallback: https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
    else:
        st.warning("Paste a URL first!")

# Sidebar params (existing)
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

if st.button("Analyze Spiral"):
    if 'df' not in st.session_state:
        st.warning("Load a dataset first—try the Iris URL above!")
        st.stop()
    
    df = st.session_state.df
    engine = SpiralEngine(sc=sc)
    params = {'td': len(df), 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da}  # TD from data size
    
    values = engine.simulate_spiral(params, iterations=iterations, sign=sign, noise_level=noise)
    
    st.subheader("Spiral Values")
    st.write(values)
    
    # Quick Data Insight (e.g., mean/std on first numeric col)
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        baseline_mean = df[col].mean()
        spiral_adjust = np.mean(values) * 0.01  # Proxy tweak from path
        st.metric("Baseline Mean", baseline_mean)
        st.metric("Spiral-Tuned Estimate", baseline_mean + spiral_adjust)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(values, marker='o', linewidth=2, label=f'{sign} Path')
    ax.set_title(f'Spiral Path Evolution on {df.shape[0]} Rows (Noise: {noise:.2f})')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Path Value')
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    
    # Narrative Summary ("Speak English")
    uplift_proxy = np.std(values) / np.mean(values) * 100  # Rough "insight gain"
    narrative = f"""
    **Quick Insight:** Your {df.shape[0]}-row dataset spirals with a {uplift_proxy:.1f}% variability edge—suggesting {iterations} cycles refine noise into signal. 
    Lean {sign} for {'exploration (wide hypotheses)' if sign == '+' else 'convergence (bias-tight focus)'}. 
    Ethical nudge: Provenance logged below—human seal recommended for pubs.
    """
    st.markdown(narrative)
    
    # Provenance
    st.subheader("Provenance Log (Last Cycle)")
    st.json(engine.get_provenance()[-1])
    
    # Export
    export_data = {
        'params': params,
        'values': values,
        'dataset_shape': df.shape,
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
    st.info("Export for sharing—load in a NB or collab with your AI pal!")

st.markdown("---")
st.write("Built with Spiral Theory—fork on GitHub, cite via Zenodo DOI: https://doi.org/10.5281/zenodo.16585562. Ethical AI: Human seal encouraged.")
