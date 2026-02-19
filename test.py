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