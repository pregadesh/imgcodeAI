import streamlit as st
import os
import tempfile
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import json
import time

from pipeline.layout_detection import detect_layout
from pipeline.style_extract import extract_styles
from pipeline.hierarchy_builder import build_hierarchy
from pipeline.code_gen import generate_html_code


def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


analysis_lottie = load_lottie_file("animation/analysi.mp4.lottie.json")
generation_lottie = load_lottie_file("animation/lizard.mp4.lottie.json")
success_lottie = load_lottie_file("animation/success.mp4.lottie.json")


st.set_page_config(page_title="Image to HTML Generator", layout="wide")
st.title("Image to HTML Generator")

api_key_input = st.text_input("API key", type="password")
if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

uploaded_file = st.file_uploader("Upload image here", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Original Image Preview")
        st.image(uploaded_file, use_column_width=True)

    if st.button("Generate", type="primary"):

        analysis_placeholder = st.empty()
        with analysis_placeholder.container():
            st.markdown("Let me take a look...")
            st_lottie(analysis_lottie, height=250, key="analysis")
            elements = detect_layout(tmp_path)
            styled_elements = extract_styles(tmp_path, elements)
            layout_tree = build_hierarchy(styled_elements)
        analysis_placeholder.empty()

        generation_placeholder = st.empty()
        with generation_placeholder.container():
            st.markdown("Pregadesh Cooking something Big....")
            st_lottie(generation_lottie, height=250, key="generation")
            generated_html = generate_html_code(layout_tree)
        generation_placeholder.empty()

        success_placeholder = st.empty()
        with success_placeholder.container():
            st.markdown("Complete!")

            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                st_lottie(success_lottie, height=200, key="success")

            st.success("Pregadesh completed the job successfully!")
            time.sleep(2)
        success_placeholder.empty()

        st.markdown("---")
        st.subheader("2. Generated Output & Preview")

        tab1, tab2 = st.tabs(["Preview", "HTML Code"])

        with tab1:
            st.markdown("### Rendering Output")
            components.html(generated_html, height=600, scrolling=True)

        with tab2:
            st.markdown("### Code")
            st.code(generated_html, language="html")
            st.download_button(
                label="Download HTML Code",
                data=generated_html,
                file_name="generated_layout.html",
                mime="text/html",
            )

        st.markdown("---")