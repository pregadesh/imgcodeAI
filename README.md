1. Objective

The objective of this project is to design a structured system that converts a screenshot of a web or mobile user interface into clean and organized HTML/CSS code.

The system avoids direct end-to-end image-to-code generation. Instead, it follows a multi-stage pipeline that explicitly detects layout elements, constructs a structured representation, extracts styling information, and then generates HTML/CSS from that structured data.

The focus is on layout understanding, hierarchy modeling, and controlled code generation.

2. Tech Stack

Frontend : Streamlit

Processing : OpenCV (Layout detection)

Pillow (Image loading and preprocessing)

NumPy

Scikit-learn (KMeans for color extraction)

Pytesseract (Text detection using OCR)

Scikit-image (visual evaluation)

Code Generation (LLM - "gemini api")

Architecture: 1.User Upload (Streamlit)

2.Layout Detection (OpenCV + OCR)

3.Hierarchy Builder (JSON Tree Construction)

4.Style Extraction (Color analysis)

5.Code Generator (LLM)

Final : Evaluation

3.Approach

Strategies:

Computer Vision for UI element detection

Rule-based spatial grouping for layout hierarchy construction

Color clustering for style extraction

JSON-based intermediate layout representation

LLM-assisted HTML generation

Visual and structural evaluation metrics

Each stage testable.

4.Workflow Stages

Stage 1: Layout Detection

Detect UI elements such as text blocks, buttons, images, and containers using computer vision techniques.

Stage 2: Layout Hierarchy Construction

Convert detected flat elements into a structured layout tree capturing parent-child relationships and row/column groupings and return as JSON layout tree.

Stage 3: Style Extraction

Extract dominant colors, font size aprox, spacing, alignment information from detected regions and return as Style mapping JSON.

Stage 4: Code Generation

Convert structured layout and style information into clean HTML/CSS code using a LLM and generated HTML file.

Stage 5: Evaluation

Measure visual similarity between the original screenshot and generated output using SSIM and structural comparison metrics.
