import os
import sys

# 1. CRITICAL: This path injection MUST run before ANY local folder imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Safe framework imports
from flask import Flask, render_template, request

# 3. Local imports (now fully visible to Python)
from api.config import GENAI_API_KEY

# Use absolute path resolution to guarantee Flask finds the template folder
app = Flask(
    __name__, 
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Lazy load the heavy AI services inside the route to avoid timeouts
    from services.genai_service import get_response

    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return render_template("index.html", error="Please enter a valid prompt.")
        
    response_html = get_response(prompt)
    return render_template("index.html", response=response_html)
