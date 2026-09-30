import time
import os
from google import genai
from google.genai import errors
# This line must come BEFORE you use the variable below!
from api.config import GENAI_API_KEY

# Initialize the modern SDK client using your imported key
client = genai.Client(api_key=GENAI_API_KEY)

def get_response(prompt):
    fixed_prompt = f"""
Answer the following question in valid HTML only.Do not include markdown, ```html blocks, <html>, <body>, or <head> tags. Use <h3> for headings, <p> for paragraphs, and <ul> with <li> for lists. Question: {prompt}"

Requirements:
- Use <h2>, <h3> headings.
- Use <p> for paragraphs.
- Use <ul><li> for bullet points.
- Use <pre><code> for code.
- Do not use Markdown.
- Do not include <html>, <body>, or <head> tags.

Question:
{prompt}
"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Request content from the model
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite", 
                contents=fixed_prompt
            )
            return response.text.strip()
            
        except Exception as e:
            # If it's a server/rate limit error, wait a moment and try again
            if ("503" in str(e) or "Server" in str(e)) and attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
                continue
            
            # Fallback error layout if all retries fail
            return """
            <h2>Service Temporarily Busy</h2>
            <p>Our AI servers are experiencing exceptionally high traffic at the moment. 
            Please wait a few seconds and try submitting your request again!</p>
            """
