import time
import google.generativeai as genai
from google.genai.errors import ServerError
from config import GENAI_API_KEY

client = genai.Client(api_key=GENAI_API_KEY)

def get_response(prompt):

    fixed_prompt=f"""
Answer the following question in valid HTML only.

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

    # Retry loop configuration (Tries up to 3 times before giving up)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite", 
                contents=fixed_prompt
            )
            return response.text.strip()
            
        except ServerError as e:
            # If it's a 503 error, wait a moment and try again
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
                continue
            
            # If all retries fail, return a polite fallback layout instead of crashing
            return """
            <h2>Service Temporarily Busy</h2>
            <p>Our AI servers are experiencing exceptionally high traffic at the moment. 
            Please wait a few seconds and try submitting your request again!</p>
            """
