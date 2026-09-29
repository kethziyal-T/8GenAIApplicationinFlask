import os
from flask import Flask, render_template, request
import google.generativeai as genai
from services.genai_service import get_response
import markdown

app = Flask(__name__)
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    prompt = request.form["prompt"]

    response = get_response(prompt)

       # Convert Markdown to HTML
    response_html = markdown.markdown(
        response,
        extensions=[
            "fenced_code",
            "tables"
        ]
    )


    return render_template(
        "result.html",
        prompt=prompt,
        response=response_html
    )


if __name__ == "__main__":
    app.run(debug=True)
    
app=app
