import sys
import os
import json
import time
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import fitz  # PyMuPDF for PDF (add to requirements.txt if missing)

# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiral_engine import SpiralEngine

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
        # RTF as text (strip tags tags roughly)
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

    if st.button("Spiral Elucidate", key="elucidate_spiral"):
        engine = SpiralEngine(sc=sc)
        params = {'td': td, 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da}
        
        values, indicators = engine.simulate_spiral_with_indicators(params, iterations=iterations, sign=sign, noise_level=noise)
        
        # Store in session_state for sharing
        st.session_state.values = values
        st.session_state.indicators = indicators
        
        st.subheader("Path Indicators")
        for ind in indicators:
            st.write(f"Cycle {ind['cycle']}: Base {ind['base']:.2f}, Adjustment {ind['adjustment']:.2f}, Value {ind['value']:.2f}")
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot([i['value'] for i in indicators], marker='o', linewidth=2, label=f'{sign} Path')
        ax.set_title(f"Elucidation Spiral (Noise: {noise:.2f})")
        ax.set_xlabel('Iteration')
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
    
    # Narrative Tune-Up (Scoped with session_state check)
    if st.button("Elucidate Narrative", key="narrative_elucidate"):
        if 'values' not in st.session_state or not st.session_state.values:
            st.warning("Run 'Spiral Elucidate' first to generate values!")
            st.stop()
        
        values = list(st.session_state.values or [])  # Force list, fallback empty
        if not values:
            st.warning("No values loaded—run Spiral Elucidate first!")
            st.stop()
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        
        # Vectorize chunks
        vectorizer = TfidfVectorizer(max_features=50)
        X = vectorizer.fit_transform(chunks)
        
        # Weight by path values (high-value cycles boost themes)
        values_array = np.asarray(values, dtype=np.float64)  # Force float64 array, robust
        sum_values = np.sum(values_array)
        sum_values = np.maximum(sum_values, 1.0)  # Clamp to avoid zero-division
        weights = values_array / sum_values  # Normalized safe
        weighted_X = X.multiply(weights.mean())  # Proxy for all cycles
        
        # Cluster for themes (k=3 for simplicity)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        theme_labels = kmeans.fit_predict(weighted_X)
        
        # Top words per theme
        feature_names = vectorizer.get_feature_names_out()
        top_themes = {}
        for i in range(3):
            cluster_words = weighted_X[theme_labels == i].mean(axis=0).A1
            top_idx = np.argsort(cluster_words)[-3:]
            top_themes[f'Theme {i+1}'] = [feature_names[idx] for idx in top_idx]
        
        # Final Summation
        core_message = f"Core theme: {', '.join(top_themes['Theme 1'])} as the arrow's foil—entropy's tyranny bent by creativity's tide."
        impact = f"Path review impact: {retention:.1f}% retention holds the narrative steady; {uplift:.1f}% uplift sharpens the philosophical edge for deeper dives."
        st.markdown(f"**Narrative Breakdown:** {core_message} {impact}")
        st.json(top_themes)
        
        st.info("Tune RF higher for tighter themes; + sign explores, - converges.")

st.markdown("---")
st.write("Built with Spiral Theory + Elucidation—fork on GitHub, cite via Zenodo DOI: https://doi.org/10.5281/zenodo.16585562. Ethical AI: Human seal encouraged.")
