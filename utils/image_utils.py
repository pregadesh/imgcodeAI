import os
import config
import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(pil_img):
    rgb_arr = np.array(pil_img)
    bgr_img = cv2.cvtColor(rgb_arr,cv2.COLOR_RGB2BGR)
    return bgr_img

def resize(img, width=None):
    if width is None or width <=0 :
        return img
    h, w = img.shape[:2]
    ratio = width/float(w)
    new_h = int(h*ratio)
    resized = cv2.resize(img,(width,new_h))
    return resized

def to_gray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def detect_edges(gray_img):

    edges = cv2.Canny(
        gray_img,
        config.EDGE_THRESHOLD_1,
        config.EDGE_THRESHOLD_2
    )
    return edges

def draw_bbox(img,boxes,color=(255,0,0),thickness=3):
    output = img.copy()
    for box in boxes:
        x1,y1,x2,y2 = box
        cv2.rectangle(output,(x1,y1),(x2,y2),color,thickness)
    return output

def save_img(path,img):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    cv2.imwrite(path,img)