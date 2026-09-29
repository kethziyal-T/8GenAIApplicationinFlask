import os
from flask import Flask, render_template, request
import google.generativeai as genai
import markdown
from google.api_core.exceptions import GoogleAPIError

# Force Flask to trace paths outside the isolated serverless function folder
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(root_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Combined Gemini Service function directly inside this file
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
    user_message = request.form.get("message", "")
    if not user_message:
        return render_template("index.html", error="Message cannot be empty")
    
    raw_ai_response = get_response(user_message)
    html_ai_response = markdown.markdown(raw_ai_response)
    
    return render_template("result.html", response=html_ai_response, user_message=user_message)

if __name__ == "__main__":
    app.run(debug=True)

app = app
