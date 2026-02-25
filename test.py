import json
from PIL import Image

from utils.image_utils import pil_to_cv2, draw_detections, save_img
from pipeline.layout_detection import layout_element
from pipeline.hierarchy_builder import tree_layout
from pipeline.style_extract import extract_styles
from pipeline.code_gen import html_gen, html_save
from pipeline.evaluation import evaluate_layout


IMG_PATH = "sample.png"
DEBUG_PATH = "output/debug_det.png"


def test():
    pil_image = Image.open(IMG_PATH).convert("RGB")
    cv_img = pil_to_cv2(pil_image)
    img_h, img_w = cv_img.shape[:2]
    print(f"Loaded {IMG_PATH}  ({img_w}x{img_h})")

    # 1. Layout detection
    detections = layout_element(cv_img)
    print(f"\n=== Stage 1: Layout Detection ({len(detections)} elements) ===")
    for d in detections:
        print(f"  #{d['id']:3d}  {d['type']:10s}  bbox={d['bbox']}"
              + (f"  \"{d['content']}\"" if d.get("content") else ""))

    debug_img = draw_detections(cv_img.copy(), detections)
    save_img(DEBUG_PATH, debug_img)
    print(f"\nDebug image saved: {DEBUG_PATH}")

    # 2. Hierarchy
    layout = tree_layout(detections, img_shape=(img_h, img_w))
    print(f"\n=== Stage 2: Hierarchy Tree ===")
    print(json.dumps(layout, indent=2))

    # 3. Styles
    styles = extract_styles(cv_img, detections)
    print(f"\n=== Stage 3: Extracted Styles ===")
    print(json.dumps(styles, indent=2))

    # 4. Code generation (rule-based, no LLM)
    html = html_gen(layout, styles)
    html_save(html)
    print(f"\n=== Stage 4: HTML generated (rule-based) ===")
    print(f"Saved to: {html_save.__module__}.GENERAL_HTML_PATH")

    # 5. Evaluation
    eval_result = evaluate_layout(layout, styles, html)
    print(f"\n=== Stage 5: Evaluation ===")
    print(json.dumps(eval_result, indent=2))
    print("\nDone ✓")


if __name__ == "__main__":
    test()