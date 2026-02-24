"""
Streamlit demo: screenshot → layout detection → hierarchy → styles → HTML/CSS → evaluation.
"""
import json
import tempfile
import os

import streamlit as st
import cv2
import numpy as np
from PIL import Image

import config
from utils.image_utils import pil_to_cv2, draw_bbox
from pipeline.layout_detection import layout_element
from pipeline.hierarchy_builder import tree_layout
from pipeline.style_extract import extract_styles
from pipeline.code_gen import html_gen, html_save, generate_html_with_llm
from pipeline.evaluation import evaluate_layout

st.set_page_config(page_title="Screenshot to HTML", layout="wide")
st.title("Screenshot → HTML Pipeline")

uploaded = st.file_uploader("Upload a screenshot (web or mobile UI)", type=["png", "jpg", "jpeg"])
use_llm = st.checkbox("Use Gemini to generate HTML (otherwise rule-based)", value=True)

if not uploaded:
    st.info("Upload an image to run the pipeline.")
    st.stop()

pil_image = Image.open(uploaded).convert("RGB")
cv_img = pil_to_cv2(pil_image)

with st.spinner("Running layout detection..."):
    detections = layout_element(cv_img)

if not detections:
    st.warning("No UI elements detected. Try another image.")
    st.stop()

boxes = [d["bbox"] for d in detections]
debug_img = draw_bbox(cv_img.copy(), boxes)
debug_img_rgb = cv2.cvtColor(debug_img, cv2.COLOR_BGR2RGB)

st.subheader("1. Layout detection (bounding boxes)")
st.image(debug_img_rgb, use_container_width=True)

with st.spinner("Building hierarchy and extracting styles..."):
    layout_tree = tree_layout(detections)
    styles = extract_styles(cv_img, detections)

col1, col2 = st.columns(2)
with col1:
    st.subheader("2. Layout tree (JSON)")
    st.json(layout_tree)
with col2:
    st.subheader("3. Extracted styles (JSON)")
    st.json(styles)

st.subheader("4. Code generation")
if use_llm:
    try:
        with st.spinner("Generating HTML with Gemini..."):
            html_str = generate_html_with_llm(layout_tree, styles)
    except Exception as e:
        st.error(f"LLM failed: {e}. Using rule-based fallback.")
        html_str = html_gen(layout_tree, styles)
else:
    html_str = html_gen(layout_tree, styles)

os.makedirs(config.OUTPUT_DIR, exist_ok=True)
html_path = config.GENERAL_HTML_PATH
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_str)
st.success(f"HTML saved to `{html_path}`")

st.subheader("5. Generated page preview")
st.components.v1.html(html_str, height=500, scrolling=True)

st.subheader("6. Evaluation")
eval_result = evaluate_layout(layout_tree, styles, html_str)
st.json(eval_result)
st.caption(
    "num_elements: from layout tree. element_types: detected UI types. "
    "html_tag_counts: tags in output. color_overlap_score: Jaccard overlap of colors (0–1)."
)
