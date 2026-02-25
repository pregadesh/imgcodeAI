def evaluate_quality(original_tree, generated_html):
    """
    Evaluates the structural similarity between the original detected elements
    and the generated HTML code.
    This is a basic heuristic approach.
    """
    score = 100
    
    def count_elements(tree, elem_type):
        count = 0
        for node in tree:
            if node.get("type") == elem_type:
                count += 1
            if "children" in node:
                count += count_elements(node["children"], elem_type)
        return count
        
    num_text_original = count_elements(original_tree, "text")
    num_containers_original = count_elements(original_tree, "container")
    
    # Heuristic: count tags in HTML
    # (A robust solution would parse HTML to a DOM tree)
    num_divs_generated = generated_html.lower().count("<div")
    num_text_tags_generated = sum(generated_html.lower().count(tag) for tag in ["<p", "<h", "<span", "<button", "<a "])
    
    # Calculate difference penalty
    if num_text_original > 0:
        text_diff = abs(num_text_original - num_text_tags_generated)
        score -= min(30, (text_diff / num_text_original) * 30)
        
    if num_containers_original > 0:
        container_diff = abs(num_containers_original - num_divs_generated)
        score -= min(20, (container_diff / num_containers_original) * 20)
        
    # Minimum score clamp
    score = max(10, score)
    
    return round(score, 2)
