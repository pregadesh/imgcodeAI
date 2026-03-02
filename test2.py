from pipeline.layout_detection import detect_layout
import cv2
import os
import numpy as np
import easyocr

os.makedirs("lay_out", exist_ok=True)

image_path = "sample.png"
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

reader = easyocr.Reader(['en'], gpu=False)

text_results = reader.readtext(gray)
img_text = img.copy()
for (bbox, text, prob) in text_results:
    tl = bbox[0]
    br = bbox[2]
    x, y = int(tl[0]), int(tl[1])
    w, h = int(br[0] - tl[0]), int(br[1] - tl[1])
    cv2.rectangle(img_text, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imwrite("lay_out/text_detection.png", img_text)

for (bbox, text, prob) in text_results:
    tl = bbox[0]
    br = bbox[2]
    x, y = int(tl[0]), int(tl[1])
    w, h = int(br[0] - tl[0]), int(br[1] - tl[1])
    cv2.rectangle(gray, (x, y), (x + w, y + h), 255, -1)

cv2.imwrite("lay_out/masked_text.png", gray)

edges = cv2.Canny(gray, 50, 150, apertureSize=3)
cv2.imwrite("lay_out/edges.png", edges)

kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)
cv2.imwrite("lay_out/dilated.png", dilated)

contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contours = img.copy()
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 20 and h > 20 and w < img.shape[1] * 0.95 and h < img.shape[0] * 0.95:
        cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imwrite("lay_out/containers.png", img_contours)

print("All stages saved in the 'lay_out' folder.")