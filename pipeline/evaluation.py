import re
from collections import Counter


def _flatten_elements(node):
    """
    Collect all elements from the layout tree into a flat list.
    """
    if not node:
        return []
    elems = []
    if isinstance(node, dict):
        elems.append(node)
        for child in node.get("children", []):
            elems.extend(_flatten_elements(child))
    elif isinstance(node, list):
        for child in node:
            elems.extend(_flatten_elements(child))
    return elems


def _html_tag_counts(html):
    """
    Count basic HTML tags as a simple structural proxy.
    """
    tags = re.findall(r"<\s*([a-zA-Z0-9]+)", html or "")
    return Counter(tag.lower() for tag in tags)


def _extract_colors_from_html(html):
    """
    Extract hex colors from inline styles / CSS in the generated HTML.
    """
    if not html:
        return set()
    matches = re.findall(r"#([0-9a-fA-F]{6})", html)
    return set("#" + m.lower() for m in matches)


def evaluate_layout(layout_tree, styles, html_str):
    """
    Simple evaluation:
    - structural: number of elements and types vs HTML tag coverage
    - visual-ish: overlap between colors in styles and colors used in HTML
    """
    elements = _flatten_elements(layout_tree)
    element_types = Counter(e.get("type", "unknown") for e in elements)

    tag_counts = _html_tag_counts(html_str)

    style_colors = set()
    for style in styles.values():
        color = style.get("background_color")
        if color:
            style_colors.add(color.lower())

    html_colors = _extract_colors_from_html(html_str)
    if style_colors or html_colors:
        intersection = style_colors & html_colors
        union = style_colors | html_colors
        color_jaccard = len(intersection) / len(union) if union else 0.0
    else:
        color_jaccard = 0.0

    return {
        "num_elements": len(elements),
        "element_types": dict(element_types),
        "html_tag_counts": dict(tag_counts),
        "color_overlap_score": round(color_jaccard, 3),
    }

