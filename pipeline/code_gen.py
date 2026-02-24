import os
import json

import config
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(config.GEMINI_MODEL)


def _build_prompt(layout_tree, styles):
    """
    Build a compact text prompt from the intermediate JSON representation.
    The LLM never sees the raw image, only this structured layout + style data.
    """
    structured_data = {
        "layout_tree": layout_tree,
        "styles": styles,
    }
    json_str = json.dumps(structured_data, indent=2)

    instructions = (
        "You are a front-end developer.\n"
        "Given a UI layout tree and per-element CSS-like styles in JSON, "
        "generate a single HTML document with embedded <style> that closely "
        "reproduces the structure and layout.\n\n"
        "Requirements:\n"
        "- Use semantic HTML tags where possible (div, p, button, a, input).\n"
        "- Use flexbox for containers (direction: row/column from the JSON).\n"
        "- Respect background colors and approximate font sizes from the JSON.\n"
        "- Do NOT include any explanations, only return valid HTML.\n\n"
        "JSON describing the layout and styles:\n"
    )
    return instructions + json_str


def generate_html_with_llm(layout_tree, styles):
    """
    Use Gemini to turn the intermediate representation into HTML/CSS.
    """
    prompt = _build_prompt(layout_tree, styles)
    response = model.generate_content(prompt)
    html = getattr(response, "text", None) or str(response)
    return html

#style builder
def style_builder(style_dict):
    if not style_dict:
        return ""
    style_part = []
    for key,value in style_dict.items():
        css_key = key.replace("_","-")
        style_part.append(f"{css_key}:{value};")
    return " ".join(style_part)

def element_render(node,style):
    element_type = node.get("type")
    bbox = node.get("bbox")
    element_id = node.get("id")

    style_dict = style.get(element_id,{}) if element_id else {}
    style_string = style_builder(style_dict)
    if element_type == "container":
        direction = node.get("direction","column")
        flex_style = {
            "display":"flex",
            "flex-direction":direction,
            "gap":"10px"
        }
        container_style = style_builder(flex_style)
        custom_style = style_builder(style_dict)
        combine_style = f"{container_style}{custom_style}".strip()
        children_html = ""

        for child in node.get("children",[]):
            children_html += element_render(child,style)
        return f'<div style ="{combine_style}">{children_html}</div>'
    # text 
    if element_type == "text":
        content = node.get("content","")
        return f'<p style="{style_string}">{content}</p>'
    #button
    if element_type == "button":
        content = node.get("content","Button")
        return f'<button style="{style_string}">{content}</button>'
    #link
    if element_type == "link":
        content = node.get("content","") 
        return f'<a href="#" style="{style_string}">{content}</a>'
    #input element
    if element_type == "input":
        return f'<input type="text" style="{style_string}"/>'
    
# HTML genrator :

def html_gen(layout_tree,styles):
    body_content = element_render(layout_tree,styles)
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Generated UI</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 40px;">
        {body_content}
    </body>
    </html>
    """
    return html_template

#save html :
def html_save(html_str):
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(config.GENERAL_HTML_PATH, "w",encoding="utf-8") as f :
        f.write(html_str)