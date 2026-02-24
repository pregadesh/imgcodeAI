import json
from PIL import Image

from utils.image_utils import pil_to_cv2,draw_bbox,save_img
from pipeline.layout_detection import layout_element
from pipeline.hierarchy_builder import tree_layout
from pipeline.style_extract import extract_styles
from pipeline.code_gen import html_gen,html_save

img_path = "sample.png"
output_path = "output/debug_det.png"


def test():
    pil_image = Image.open(img_path)
    cv_img = pil_to_cv2(pil_image)
    print("Loaded")

    detections = layout_element(cv_img)
    for d in detections:
        print(d)
    boxes = [d["bbox"]for d in detections]
    debug_img = draw_bbox(cv_img,boxes)

    save_img(output_path,debug_img)
    print(f"Debug image are savedin : {output_path}")
    #style extracted
    styles = extract_styles(cv_img,detections)
    print("\nStyle:")
    print(json.dumps(styles,indent=1))
    #laout extracted
    layout = tree_layout(detections)
    print(f"tree is generated")
    print(json.dumps(layout,indent=1))
    html = html_gen(layout,styles)
    html_save(html)
    print()
test()

'''
#layout_detection
from pipeline.layout_detection import layout_element
import cv2
img = cv2.imread("sample.png")
res = layout_element(img)
print(res)
'''

'''
#image_utils.py
from PIL import Image
from utils.image_utils import (
    pil_to_cv2,
    resize,
    to_gray,
    detect_edges,
    draw_bbox,
    save_img
)
pil_img = Image.open("sample.png")
cv_img = pil_to_cv2(pil_img)
print("PIL open ok :", cv_img.shape)

resized = resize(cv_img,width=500)
print("Resize", resized.shape)

grayscale= to_gray(resized)
print("grayscale",grayscale.shape)

edge_detect = detect_edges(grayscale)
print("edge finder : ",edge_detect.shape)

boxes  =[(50,50,200,200)]
boxed = draw_bbox(resized,boxes)

save_img("output/resized.jpg", resized)
save_img("output/gray.jpg", grayscale)
save_img("output/edges.jpg", edge_detect)
save_img("output/boxed.jpg", boxed)
print("all done")
'''