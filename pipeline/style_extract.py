import cv2
import numpy as np
from sklearn.cluster import KMeans
import config


def bgr_to_hex(color):
    b, g, r = int(color[0]), int(color[1]), int(color[2])
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def extract_dominant_color(region):
    pixels = region.reshape((-1, 3))

    kmeans = KMeans(
        n_clusters=config.KMEANS_CLUSTERS,
        n_init=10
    )

    kmeans.fit(pixels)

    counts = np.bincount(kmeans.labels_)
    dominant_color = kmeans.cluster_centers_[np.argmax(counts)]

    return bgr_to_hex(dominant_color)


def estimate_font_size(bbox):
    _, y1, _, y2 = bbox
    height = y2 - y1

    font_size = int(height * config.FONT_SIZE_SCALE)

    return f"{font_size}px"


def extract_styles(image, detections):
    styles = {}

    for element in detections:
        element_id = element["id"]
        x1, y1, x2, y2 = element["bbox"]

        region = image[y1:y2, x1:x2]

        if region.size == 0:
            continue

        dominant_color = extract_dominant_color(region)
        font_size = estimate_font_size(element["bbox"])

        styles[element_id] = {
            "background_color": dominant_color,
            "font_size": font_size
        }

    return styles
