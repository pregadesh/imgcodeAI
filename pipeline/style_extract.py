import cv2
import numpy as np

def extract_styles(image_path, elements):
    """
    Extracts basic styles (e.g., background color) for the detected elements.
    """
    img = cv2.imread(image_path)
    if img is None:
        return elements

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    styled_elements = []
    for el in elements:
        x, y, w, h = el["bbox"]
        
        # Crop the region
        # Make sure bounding box is within image bounds
        x = max(0, x)
        y = max(0, y)
        roi = img_rgb[y:y+h, x:x+w]
        
        style = {}
        
        if roi.size > 0:
            # Simple approach: get the median color as background color
            median_color = np.median(roi, axis=(0, 1))
            hex_color = '#{:02x}{:02x}{:02x}'.format(int(median_color[0]), int(median_color[1]), int(median_color[2]))
            style["background_color"] = hex_color
            
            # Very rough font size estimation
            if el["type"] == "text":
                style["font_size"] = f"{int(h * 0.6)}px"
                
        new_el = el.copy()
        new_el["style"] = style
        styled_elements.append(new_el)
        
    return styled_elements
