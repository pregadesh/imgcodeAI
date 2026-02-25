import cv2
import easyocr
import numpy as np

# Initialize EasyOCR reader once to save loading time
reader = easyocr.Reader(['en'], gpu=False)

def detect_layout(image_path):
    """
    Detects layout elements (containers, text) in an image.
    Returns a list of dictionaries, each representing an element.
    """
    img = cv2.imread(image_path)
    if img is None:
        return []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Detect text using EasyOCR
    text_results = reader.readtext(gray)
    elements = []
    
    for (bbox, text, prob) in text_results:
        # EasyOCR returns bbox as a list of 4 points: [tl, tr, br, bl]
        # We convert it to (x, y, w, h)
        tl = bbox[0]
        br = bbox[2]
        x, y = int(tl[0]), int(tl[1])
        w, h = int(br[0] - tl[0]), int(br[1] - tl[1])
        
        elements.append({
            "type": "text",
            "bbox": [x, y, w, h],
            "content": text,
            "confidence": prob
        })
        
        # Mask out text regions so contour detection doesn't pick them up as separate containers
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), -1)
        
    # 2. Detect containers (images, buttons, inputs) using OpenCV contours
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Dilate to connect broken edges
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Filter out very small or very large containers
        if w > 20 and h > 20 and w < img.shape[1] * 0.95 and h < img.shape[0] * 0.95:
            elements.append({
                "type": "container",
                "bbox": [x, y, w, h],
                "content": ""
            })
            
    return elements
