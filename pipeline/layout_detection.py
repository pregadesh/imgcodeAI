import cv2
import numpy as np
import pytesseract
import config
from utils.image_utils import to_gray,detect_edges

def pre_process_ocr(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(3,3),0)
    thresh = cv2.adaptiveThreshold(
        gray,255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,2
    )
    return thresh

def detect_shape_elements(img):
    gray_img = to_gray(img)
    edges = detect_edges(gray_img)

    contoures,_ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    detections = []
    element_id = 1
    for contour in contoures:
        area = cv2.contourArea(contour)
        if area<config.MIN_CONTOUR_AREA:continue
        if area > config.MAX_CONTOUR_AREA: continue
        a,b,c,d = cv2.boundingRect(contour)
        aspect_ratio = c / float(d)

        element_type = "container"

        if aspect_ratio >= config.INPUT_ASPECT_RATIO_MIN: element_type = "input"
        if aspect_ratio >= config.BUTTON_ASPECT_RATIO_MIN : element_type = "button"

        detections.append({
            "id": element_id,
            "type": element_type,
            "bbox":[a,b,a+c,b+d]
        })
        element_id += 1
    return detections

def text_semantic(img,bbox):
    x1,y1,x2,y2 = bbox
    region = img[y1:y2,x1:x2]
    if region.size == 0 : return "text"
    avg_color = np.mean(region.reshape(-1, 3), axis=0)
    b,g,r = avg_color

    if b > r and b > g : return "link"
    return "text"



def detect_text_elements(img,start_id=1000):
    processed = pre_process_ocr(img)
    data = pytesseract.image_to_data(
        processed,
        output_type=pytesseract.Output.DICT
    )
    text_element = []
    current_id = start_id

    for n in range(len(data["text"])):
        text = data["text"][n].strip()
        try:
            conf = int(data["conf"][n])
        except: 
            continue
        if conf<config.OCR_CONFIDENCE_THRESHOLD: continue
        if text == "": continue

        a = data["left"][n]
        b = data["top"][n]
        c = data["width"][n]
        d = data["height"][n]
        bbox = [a,b,a+c,b+d]
        text_type = text_semantic(img,bbox)
        text_element.append({
            "id":current_id,
            "type": text_type,
            "content":text,
            "bbox" : [a,b,a+c,b+d]
        })
        current_id += 1
    return combine_text(text_element)

def combine_text(text_element):
    merged = []
    used = set()
    for i ,elem in enumerate(text_element):
        if i in used : continue
        x1,y1,x2,y2 = elem["bbox"]
        content = elem["content"]
        for j, x in enumerate(text_element):
            if j <= i or j in used : continue
            ox1,oy1,ox2,oy2 = x["bbox"]
            if abs(y1 - oy1) < config.OCR_MERGE_Y_THRESHOLD:
                if abs(x2 - ox1) < config.OCR_MERGE_X_THRESHOLD:
                    content += " " + x["content"]
                    x2 = ox2
                    used.add(j)
        merged.append({
            "id":elem["id"],
            "type":elem["type"],
            "content":content,
            "bbox":[x1,y1,x2,y2]
        })
    return merged

def layout_element(img):
    shape_ele = detect_shape_elements(img)
    text_ele = detect_text_elements(img,start_id=len(shape_ele)+1)
    return shape_ele + text_ele