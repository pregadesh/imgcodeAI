import cv2
import numpy as np
import config
from utils.image_utils import to_gray,detect_edges

def element_classifier(w,h,area):
    if h == 0 :
        return "unkown"
    aspect_ratio = w/float(h)
    if area > config.CONTAINER_AREA_THRESHOLD: return "container"
    if aspect_ratio >= config.INPUT_ASPECT_RATIO_MIN : return "input"
    elif aspect_ratio >= config.BUTTON_ASPECT_RATIO_MIN: return "button"
    if area < 5000: return "text"
    return "unknown"
def layout_element(img):
    gray_img = to_gray(img)
    edge = detect_edges(gray_img)

    contours,_ = cv2.findContours(
        edge,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    detections = []
    element_id = 1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < config.MIN_CONTOUR_AREA: continue
        if area > config.MAX_CONTOUR_AREA : continue
        a,b,c,d = cv2.boundingRect(contour)
        element_type = element_classifier(c,d,area)

        detection = {
            "id":element_id,
            "type":element_type,
            "bbox":[a,b,a+c,b+d],
            "area": area
        }

        detections.append(detection)
        element_id += 1
    return detections
