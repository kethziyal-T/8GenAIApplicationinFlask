import os
import sys
from flask import Flask, render_template, request
import google.generativeai as genai
import markdown
from google.api_core.exceptions import GoogleAPIError

# MAGIC FIX: Forces Python to know exactly where your files are hidden on Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
template_dir = os.path.join(root_dir, 'templates')
sys.path.append(root_dir)

app = Flask(__name__, template_folder=template_dir)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_response(prompt):
    fixed_prompt = f"Answer the following question in valid HTML only.\n\nQuestion:\n{prompt}"
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(fixed_prompt)
        return response.text.strip()
    except GoogleAPIError as e:
        return f"<p>Error communicating with Gemini AI: {str(e)}</p>"
    except Exception as e:
        return f"<p>An unexpected error occurred: {str(e)}</p>"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # MAGIC FIX 2: Reads both 'message' or 'prompt' inputs safely
    user_message = request.form.get("message") or request.form.get("prompt") or ""
    if not user_message:
        return render_template("index.html", error="Message cannot be empty")
    
    raw_ai_response = get_response(user_message)
    html_ai_response = markdown.markdown(raw_ai_response)
    
    return render_template("result.html", response=html_ai_response, user_message=user_message)

if __name__ == "__main__":
    app.run(debug=True)

app = app
