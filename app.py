# app.py - Flask web interface (teen models)
# Local chalane ke liye:  python app.py   phir browser mein http://127.0.0.1:5000

import os

import joblib
from flask import Flask, render_template, request

from text_utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
if not os.path.exists(os.path.join(TEMPLATE_DIR, "index.html")):
    TEMPLATE_DIR = BASE_DIR  # agar upload mein 'templates' folder na bane to bhi page chale

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# train_models.py se bani file: vectorizer + teen models + scores
bundle = joblib.load(os.path.join(BASE_DIR, "models.pkl"))
vectorizer = bundle["vectorizer"]
models = bundle["models"]


@app.route("/", methods=["GET", "POST"])
def home():
    comment, error, note, results = "", "", "", []
    if request.method == "POST":
        comment = request.form.get("comment", "")[:500]
        cleaned = clean_text(comment)  # same cleaning jo training mein thi
        if not cleaned:
            error = "Please enter a valid Roman Urdu comment"
        else:
            features = vectorizer.transform([cleaned])
            if features.nnz == 0:
                note = "Ye alfaaz training data mein nahi hain, is liye jawab par bharosa kam karein."
            for name, model in models.items():
                abusive = int(model.predict(features)[0]) == 1  # 1 = Abusive
                results.append({"name": name, "abusive": abusive})
    return render_template(
        "index.html", comment=comment, error=error, note=note, results=results,
        metrics=bundle["metrics"], matrices=bundle["matrices"], test_size=bundle["test_size"],
    )


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
