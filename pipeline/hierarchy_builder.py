import config
def get_top_left(bbox):
    x1,y1,_,_ = bbox
    return x1,y1
def sort_elements(elements):
    def sort_key(element):
        y = element["bbox"][1] #top value
        x = element["bbox"][0] #left value
        return (y,x)
    return sorted(elements,key=sort_key)
def grp_rows(elements):
    rows = []
    used = set()
    for i,ele in enumerate(elements):
        if i in used: continue
        x1,y1,x2,y2 = ele["bbox"]
        current_row = [ele]
        used.add(i)
        for j,x in enumerate(elements):
            if j in used : continue
            _,oy1,_,_ = x["bbox"]
            if abs(y1-oy1)<config.ROW_ALIGNMENT_THRESHOLD:
                current_row.append(x)
                used.add(j)
        rows.append(current_row)
    return rows

def tree_layout(detections):
    if not detections:
        return{}
    sorted_elements = sort_elements(detections)
    grouped_rows = grp_rows(sorted_elements)

    root = {
        "type":"container",
        "direction":"column",
        "children":[]
    }

    for group in grouped_rows:
        if len(group) >= config.MIN_GROUP_SIZE:
            row_container= {
                "type":"container",
                "direction":"row",
                "children":group
            }
            root["children"].append(row_container)
        else:
            root["children"].append(group[0])
    return root
