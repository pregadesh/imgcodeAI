def is_inside(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Check if center of box1 is inside box2 as a simple heuristic
    cx1, cy1 = x1 + w1 / 2, y1 + h1 / 2
    
    return (x2 <= cx1 <= x2 + w2) and (y2 <= cy1 <= y2 + h2)

def build_hierarchy(elements):
    #Constructs a JSON layout tree from a flat list of elements.
    # sort elements by area desec (L file first)
    elements = sorted(elements, key=lambda el: el["bbox"][2] * el["bbox"][3], reverse=True)
    
    # each node adds a 'children' list
    for el in elements:
        el["children"] = []
        
    tree = []
    
    for i, child_el in enumerate(elements):
        parent_found = False
        # check the smallest parent that contains this child
        # iterate backwards from the current index to get imeediate container 
        for j in range(i - 1, -1, -1):
            parent_el = elements[j]
            if is_inside(child_el["bbox"], parent_el["bbox"]):
                parent_el["children"].append(child_el)
                parent_found = True
                break
                
        if not parent_found:
            # If no parent found then its root element
            tree.append(child_el)
            
    return tree
