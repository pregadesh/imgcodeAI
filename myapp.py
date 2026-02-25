import streamlit as st
import os
import tempfile
import streamlit.components.v1 as components

# Import custom pipeline modules
from src.layout_detection import detect_layout
from src.style_extraction import extract_styles
from src.hierarchy_construction import build_hierarchy
from src.code_generation import generate_html_code
from src.evaluation import evaluate_quality

st.set_page_config(page_title="Image to HTML Generator", layout="wide")

st.title("📸 Image to HTML Generator Pipeline")
st.markdown("Upload a screenshot to extract layout elements, build a hierarchy, and generate responsive HTML/CSS.")

# Sidebar for config
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Gemini API Key", type="password", help="Overrides .env GEMINI_API_KEY")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        
    st.markdown("---")
    st.markdown("### Pipeline Steps:")
    st.markdown("1. Layout Detection (OpenCV & EasyOCR)")
    st.markdown("2. Style Extraction (Color/Font size)")
    st.markdown("3. Hierarchy Construction (JSON Tree)")
    st.markdown("4. Code Generation (Gemini LLM)")

uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the uploaded file into a temporary file so OpenCV can read it via path
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Original Image Preview")
        st.image(uploaded_file, use_column_width=True)
        
    if st.button("Run Pipeline & Generate HTML", type="primary"):
        with st.spinner("Step 1/3: Detecting Layout & Styles..."):
            elements = detect_layout(tmp_path)
            styled_elements = extract_styles(tmp_path, elements)
            layout_tree = build_hierarchy(styled_elements)
            
        with st.spinner("Step 2/3: Generating HTML/CSS using Gemini..."):
            generated_html = generate_html_code(layout_tree)
            
        with st.spinner("Step 3/3: Evaluating Results..."):
            score = evaluate_quality(layout_tree, generated_html)
            
        st.success("Pipeline completed successfully!")
        
        st.markdown("---")
        
        st.subheader("2. Generated Output & Preview")
        
        tab1, tab2, tab3 = st.tabs(["HTML Preview", "Raw HTML Code", "JSON Layout Tree"])
        
        with tab1:
            st.markdown("### Rendering Output")
            # Render the generated HTML in Streamlit
            components.html(generated_html, height=600, scrolling=True)
            
        with tab2:
            st.markdown("### Code")
            st.code(generated_html, language='html')
            st.download_button(
                label="Download HTML Code",
                data=generated_html,
                file_name="generated_layout.html",
                mime="text/html"
            )
            
        with tab3:
            st.markdown("### Computer Vision Extracted Layout (Input to LLM)")
            st.json(layout_tree)
            
        st.markdown("---")
        
        st.subheader("💡 Evaluation Score")
        st.metric(label="Structural Fidelity Accuracy", value=f"{score}%", help="Based on comparing extracted components vs generated HTML tags.")
