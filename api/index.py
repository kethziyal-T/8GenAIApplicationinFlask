import os
import sys

# Adds the parent directory (root folder) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now your existing imports will work correctly on Vercel
import config
from services.genai_service import ...
from flask import Flask, render_template, request
# Import your background service
from services.genai_service import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    # Safeguard against empty or missing prompt submissions
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return render_template("index.html", error="Please enter a valid prompt.")

    # Get the raw HTML string directly from your service file
    response_html = get_response(prompt)

    # Return the clean prompt and HTML directly to your results page
    return render_template(
        "result.html",
        prompt=prompt,
        response=response_html
    )


if __name__ == "__main__":
    app.run(debug=True)
