from pipeline.layout_detection import detect_layout
from pipeline.hierarchy_builder import build_hierarchy
import json

image_path = "sample.png"

elements = detect_layout(image_path)
tree = build_hierarchy(elements)

def print_tree(nodes, level=0):
    for node in nodes:
        print("  " * level + f"{node['type']} -> {node['bbox']}")
        if node["children"]:
            print_tree(node["children"], level + 1)

print("JSON Output:\n")
print(json.dumps(tree, indent=4))
