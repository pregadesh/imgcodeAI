1.Tech Stack

Frontend

Streamlit (User interface for uploading screenshots and viewing results)

Backend / Core Processing

Python (Core language)

OpenCV (Layout detection and contour extraction)

Pillow (Image loading and preprocessing)

NumPy (Matrix operations)

Scikit-learn (KMeans for color extraction)

Pytesseract (Text detection using OCR)

Scikit-image (SSIM for visual evaluation)

Code Generation

Template-based HTML builder

Optional controlled LLM API (only after structured representation is created)

2.Approach

The system follows a modular compiler-style architecture instead of a direct black-box generation method.

Key strategies used:

Computer Vision for UI element detection

Rule-based spatial grouping for layout hierarchy construction

Color clustering for style extraction

JSON-based intermediate layout representation

Template-driven or controlled LLM-assisted HTML generation

Visual and structural evaluation metrics

Each stage is independent and testable.

3.Workflow Stages
Stage 1: Layout Detection

Detect UI elements such as text blocks, buttons, images, and containers using computer vision techniques.
Output: Bounding boxes with element classification.

Stage 2: Layout Hierarchy Construction

Convert detected flat elements into a structured layout tree capturing parent-child relationships and row/column groupings.
Output: JSON layout tree.

Stage 3: Style Extraction

Extract dominant colors, font size approximations, spacing, and alignment information from detected regions.
Output: Style mapping JSON.

Stage 4: Code Generation

Convert structured layout and style information into clean HTML/CSS code using a template engine or controlled LLM.
Output: Generated HTML file.

Stage 5: Evaluation

Measure visual similarity between the original screenshot and generated output using SSIM and structural comparison metrics.

4.Architecture
User Upload (Streamlit)
          ↓
Layout Detection (OpenCV + OCR)
          ↓
Hierarchy Builder (Tree Construction)
          ↓
Style Extraction (Color + Spacing Analysis)
          ↓
Code Generator (Template / LLM)
          ↓
Evaluation (SSIM + Structural Matching)

The architecture is modular, extensible, and designed for clarity and explainability rather than black-box generation.