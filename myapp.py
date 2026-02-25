import streamlit as st
import os
import tempfile
import streamlit.components.v1 as components

from pipeline.layout_detection import detect_layout
from pipeline.style_extract import extract_styles
from pipeline.hierarchy_builder import build_hierarchy
from pipeline.code_gen import generate_html_code
#from pipeline.evaluation import evaluate_quality

st.set_page_config(page_title="Image to HTML Generator", layout="wide")

st.title("Image to HTML Generator")
st.markdown("Upload a screenshot.")

with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Gemini API Key", type="password", help="Overrides .env GEMINI_API_KEY")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        
    #st.markdown("---")
    #st.markdown("### Pipeline Steps:")
    #st.markdown("1. Layout Detection (OpenCV & EasyOCR)")
    #st.markdown("2. Style Extraction (Color/Font size)")
    #st.markdown("3. Hierarchy Construction (JSON Tree)")
    #st.markdown("4. Code Generation (Gemini LLM)")

uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Original Image Preview")
        st.image(uploaded_file, use_column_width=True)
        
    if st.button("Generate", type="primary"):
        with st.spinner("1. Analysis style and structure"):
            elements = detect_layout(tmp_path)
            styled_elements = extract_styles(tmp_path, elements)
            layout_tree = build_hierarchy(styled_elements)
            
        with st.spinner("2. Generating"):
            generated_html = generate_html_code(layout_tree)
            
            
        st.success("Completed successfully!")
        
        st.markdown("---")
        
        st.subheader("2.Generated Output & Preview")
        
        tab1, tab2, tab3 = st.tabs(["HTML Preview", "Raw HTML Code", "JSON Layout Tree"])
        
        with tab1:
            st.markdown("### Rendering Output")
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
            st.markdown("layout to LLM ")
            st.json(layout_tree)
            
        st.markdown("---")
