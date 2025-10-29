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
        
        # Calculate and store retention/uplift with fallback
        if len(values) > 1:
            std_val = np.std(values)
            mean_val = np.mean(values)
            retention = 100 - (std_val / mean_val * 100) if mean_val != 0 else 100.0
            uplift = (values[-1] - values[0]) / values[0] * 100 if values[0] != 0 else 0.0
        else:
            retention = 100.0
            uplift = 0.0
        st.session_state.retention = retention
        st.session_state.uplift = uplift
        
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
        
        # Narrative Pairing (Dynamic Responses)
        avg_base = np.mean([ind['base'] for ind in indicators])
        adj_var = np.var([ind['adjustment'] for ind in indicators])
        retention = 100 - (np.std(values) / np.mean(values) * 100)
        uplift = (values[-1] - values[0]) / values[0] * 100
        
        # 5 Standard Responses (Tune thresholds as needed)
        responses = {
            'high_tension': "Graph shows high base ({avg_base:.1f})—tension buildup in core chunks; more RF (try 1.8+) to prune and release blockage for clearer locution.",
            'low_adjustment': "Low adjustment variance ({adj_var:.3f}) suggests stable flow; less DA (try 1.5) to find subtle locution shifts without over-exploring.",
            'high_retention': "Strong retention ({retention:.1f}%) holds the narrative tight; more TW (try 2.5) to amplify uplift ({uplift:.1f}%) and unlock deeper insights.",
            'low_uplift': "Modest uplift ({uplift:.1f}%) indicates convergent path; less noise (try 0.02) or switch to + sign to stir locution for bolder release.",
            'balanced': "Balanced spiral (retention {retention:.1f}%, uplift {uplift:.1f}%)—tune CIR up (try 2.0) to sustain the flow and spot hidden locution in the chunks."
        }
        
        # Pick response based on indicators (thresholds for demo—tune to your data)
        if avg_base > 450:
            response = responses['high_tension'].format(avg_base=avg_base)
        elif adj_var < 0.1:
            response = responses['low_adjustment'].format(adj_var=adj_var)
        elif retention > 95:
            response = responses['high_retention'].format(avg_base=avg_base, retention=retention, uplift=uplift)
        elif uplift < 1.0:
            response = responses['low_uplift'].format(uplift=uplift)
        else:
            response = responses['balanced'].format(retention=retention, uplift=uplift)
        
        st.markdown(f"**Dynamic Insight:** {response}")
        st.info("These tune suggestions help release blockage (stuck ideas) and spotlight locution (key phrases)—plug into an LLM for deeper riff.")

        # Export (include response)
        export_data = {
            'params': params,
            'indicators': indicators,
            'values': values,
            'sign': sign,
            'iterations': iterations,
            'noise_level': noise,
            'retention_pct': retention,
            'uplift_pct': uplift,
            'dynamic_response': response
        }
        st.download_button(
            label="Save Elucidation (JSON)",
            data=json.dumps(export_data, indent=2),
            file_name=f"spiral_{int(time.time())}.json",
            mime="application/json"
        )
        st.info("Export for sharing—drop into a NB or LLM for full riff.")

    # Narrative Tune-Up (Scoped with session_state check)
    if st.button("Elucidate Narrative", key="narrative_elucidate"):
        if 'values' not in st.session_state or not st.session_state.values:
            st.warning("Run 'Spiral Elucidate' first to generate values!")
            st.stop()
        
        values = st.session_state.values  # Pull the list, not method
        
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
