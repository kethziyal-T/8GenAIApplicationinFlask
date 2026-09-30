import os
from google import genai
from api.config import GENAI_API_KEY

# Initialize the correct SDK client handler
client = genai.Client(api_key=GENAI_API_KEY)

def get_response(prompt):
    # This formats your request strictly as clean HTML strings
    fixed_prompt = f"Answer the following question in valid HTML only. Do not include markdown, ```html blocks, <html>, <body>, or <head> tags. Use <h3> for headings, <p> for paragraphs, and <ul> with <li> for lists. Question: {prompt}"
    
    # Direct cloud execution call mapping directly to the client instance
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=fixed_prompt
    )
    
    return response.text.strip()


 
