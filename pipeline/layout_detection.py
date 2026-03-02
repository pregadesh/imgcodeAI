import cv2
import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def detect_layout(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect text using EasyOCR
    text_results = reader.readtext(gray)
    elements = []
    
    for (bbox, text, prob) in text_results:
        # EasyOCR returns bbox as a list of 4 points and convert it to (x, y, w, h)
        tl = bbox[0] #top left 
        br = bbox[2] #bottom right
        x, y = int(tl[0]), int(tl[1]) # x left post and y top pos
        w, h = int(br[0] - tl[0]), int(br[1] - tl[1]) # width and height of bbox
        
        elements.append({
            "type": "text",
            "bbox": [x, y, w, h],
            "content": text,
            "confidence": prob
        })
        
        # Mask out text regions so contour detection doenst pick them up as separate containers
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), -1) #rigt , bottom ,color, thickness
        
    # 2. Detect containers using opencv and i hv used canny algo for edge decte
    edges = cv2.Canny(gray, 50, 150, apertureSize=3) 
    
    kernel = np.ones((3,3), np.uint8) #uint for pixle type 0 to 255
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    #inner take and ess point
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#RETR = outer contours
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Filter with very small or very large containers
        if w > 20 and h > 20 and w < img.shape[1] * 0.95 and h < img.shape[0] * 0.95:
            elements.append({
                "type": "container",
                "bbox": [x, y, w, h],
                "content": ""
            })
            
    return elements
