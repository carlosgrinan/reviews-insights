import os
from dotenv import load_dotenv
from flask import Flask, app, render_template, request

from google.google_api import SCOPES, Gmail, get_token, google_maps
from openai import summarize

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html", context={"client_id": os.getenv("CLIENT_ID"), "scopes": SCOPES}
    )


@app.route("/oauth", methods=["POST"])
def post_endpoint():
    code = request.form.get("code")
    refresh_token = get_token(code)
    gmail = Gmail(refresh_token)
    emails_text = gmail.get_emails()
    summary = summarize(emails_text, type_of_text="customer support emails")
    return summary


@app.route("/reviews", methods=["GET"])
def reviews():
    reviews_text = google_maps()
    summary = summarize(reviews_text)
    return summary


if __name__ == "__main__":
    app.run(debug=True)
