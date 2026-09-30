import os
from google import genai

def get_response(prompt):
    # 💡 THE ULTIMATE FIX: Fetch the API variable directly here with an absolute fallback
    api_key = os.environ.get("GENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or ""
    
    # Initialize the client securely right inside the function block execution channel
    client = genai.Client(api_key=api_key)
    
    fixed_prompt = f"Answer the following question in valid HTML only. Do not include markdown, ```html blocks, <html>, <body>, or <head> tags. Use <h3> for headings, <p> for paragraphs, and <ul> with <li> for lists. Question: {prompt}"
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=fixed_prompt
        )
        return response.text.strip()
    except Exception as e:
        # Returns the raw text string if anything fails so the web app NEVER crashes with a 500
        return f"<h2>Application Notice</h2><p>Could not process request. Technical detail: {str(e)}</p>"


 
