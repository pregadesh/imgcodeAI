import google.generativeai as genai
import os
import json
import re

def generate_html_code(layout_tree):
    """
    Calls the Gemini API to generate HTML/CSS from the structured layout tree.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "<p style='color:red;'>Error: Gemini API Key not found or invalid in environment.</p>"
        
    genai.configure(api_key=api_key)
    
    # Ensure we use a model good with code
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    tree_str = json.dumps(layout_tree, indent=2)
    
    prompt = f"""
You are an expert Frontend Developer.
I have extracted a layout tree from a UI screenshot using computer vision.
Here is the JSON representation of the layout tree, containing 'text' and 'container' elements, along with their bounding boxes [x, y, w, h] and basic styles:

{tree_str}

Please generate clean, responsive HTML and CSS to recreate this layout as accurately as possible. 
Requirements:
1. Provide ONLY valid HTML code. Do NOT wrap it in markdown block quotes (```html) or provide any conversational text.
2. Put CSS inside a <style> block in the <head>.
3. Use Flexbox/Grid for layout where appropriate. Try to respect the relative spatial positioning based on the bounding boxes.
4. Output cleanly and strictly within Google Gemini token limits. Focus on structure over pixel-perfection.
"""

    try:
        response = model.generate_content(prompt)
        # Strip potential markdown code blocks if the model ignores our instruction
        html_code = response.text
        html_code = re.sub(r'^```html\s*', '', html_code)
        html_code = re.sub(r'\s*```$', '', html_code)
        return html_code
    except Exception as e:
        return f"<p style='color:red;'>Error during generation: {str(e)}</p>"
