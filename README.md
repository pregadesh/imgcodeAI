# Screenshot → HTML Pipeline

A multi-stage AI system that converts UI screenshots into clean HTML/CSS code. This is **not** an end-to-end LLM approach — the pipeline uses distinct computer-vision and NLP stages with a structured intermediate representation.

## Architecture

```
Screenshot (PNG/JPG)
      │
      ▼
┌─────────────────────────┐
│  1. Layout Detection    │  OpenCV contours + Tesseract OCR
│     (layout_detection)  │  → bounding boxes + element types
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│  2. Hierarchy Builder   │  Spatial containment analysis
│     (hierarchy_builder) │  → nested JSON layout tree
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│  3. Style Extraction    │  KMeans colour clustering + edge analysis
│     (style_extract)     │  → per-element CSS properties
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│  4. Code Generation     │  Gemini LLM (or rule-based fallback)
│     (code_gen)          │  → self-contained HTML/CSS file
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│  5. Evaluation          │  Color overlap, SSIM, depth, coverage
│     (evaluation)        │  → quality metrics JSON
└─────────────────────────┘
```

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| UI Detection    | OpenCV, Tesseract OCR               |
| Style Analysis  | scikit-learn (KMeans)               |
| Code Generation | Google Gemini (generative AI)       |
| Evaluation      | scikit-image (SSIM), NumPy          |
| Frontend        | Streamlit                           |
| Container       | Docker + Docker Compose             |

## Project Structure

```
├── app.py                   # Streamlit web application
├── config.py                # All tuneable thresholds & settings
├── test.py                  # CLI test script (no Streamlit)
├── pipeline/
│   ├── layout_detection.py  # Stage 1 — contour + OCR detection
│   ├── hierarchy_builder.py # Stage 2 — spatial containment tree
│   ├── style_extract.py     # Stage 3 — colour, border, font extraction
│   ├── code_gen.py          # Stage 4 — LLM / rule-based HTML gen
│   └── evaluation.py        # Stage 5 — quality metrics
├── utils/
│   └── image_utils.py       # Image conversion, bbox utilities
├── outputs/                 # Generated HTML files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                     # GEMINI_API_KEY=your_key_here
```

## Quick Start

### 1. Local setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
echo "GEMINI_API_KEY=your_key" > .env

# Run the app
streamlit run app.py
```

### 2. Docker

```bash
# Build and run
docker compose up --build

# Open http://localhost:8501
```

### 3. CLI test (no Streamlit)

```bash
python test.py
# Outputs debug image to output/ and HTML to outputs/
```

## Pipeline Details

### Stage 1 — Layout Detection
- **Preprocessing**: Morphological closing + adaptive thresholding to get clean rectangular shapes
- **Contour detection**: `cv2.findContours` with `RETR_TREE` for nested elements
- **Element classification**: Multi-signal (aspect ratio + area + colour) to distinguish buttons, inputs, containers, images
- **OCR**: Tesseract for text regions, with line-level merging by vertical centre overlap
- **Deduplication**: IoU-based suppression removes overlapping detections; OCR text is fused into shape elements

### Stage 2 — Hierarchy Construction
- **Spatial containment**: If bbox A fully contains bbox B, B becomes a child of A (smallest enclosing parent wins)
- **Row grouping**: Sibling elements with aligned vertical centres are wrapped in row containers
- **Output**: Nested JSON tree with position and dimension metadata

### Stage 3 — Style Extraction
- **Colours**: KMeans clustering extracts dominant (background) and secondary (text) colours per element
- **Borders**: Edge density analysis at boundary vs interior detects visible borders
- **Border radius**: Corner pixel analysis estimates roundedness
- **Contrast correction**: Ensures text colour contrasts with background

### Stage 4 — Code Generation
- **LLM mode** (default): Gemini receives the JSON layout tree + styles with a detailed 13-rule prompt. Response is cleaned (markdown fences stripped).
- **Rule-based fallback**: Generates HTML with `<style>` block, absolute positioning from bbox coordinates, CSS class per element.

### Stage 5 — Evaluation
- **Color overlap**: Jaccard similarity between extracted vs generated colours
- **BBox coverage**: Fraction of image area covered by detected elements
- **Hierarchy depth**: Layout tree depth vs HTML nesting depth
- **SSIM** (optional): Structural similarity between original and rendered screenshots

## Configuration

All tuneable parameters are in `config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MORPH_KERNEL_SIZE` | 5 | Morphological closing kernel |
| `MIN_CONTOUR_AREA` | 500 | Minimum contour area to keep |
| `MAX_CONTOUR_AREA` | 500000 | Maximum contour area |
| `IOU_SUPPRESSION_THRESHOLD` | 0.5 | IoU threshold for deduplication |
| `OCR_CONFIDENCE_THRESHOLD` | 50 | Minimum Tesseract confidence |
| `KMEANS_CLUSTERS` | 3 | Colour clusters per element |
| `GEMINI_MODEL` | gemini-2.5-flash | Gemini model name |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes (for LLM mode) | Google AI Studio API key |
