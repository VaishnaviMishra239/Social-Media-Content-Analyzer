from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
import fitz
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from collections import Counter
import re

# ---------------------------
# NLTK setup
# ---------------------------
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# ---------------------------
# Flask app setup
# ---------------------------
# Set static_folder to frontend/build for React
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------------------
# Text Extraction Function
# ---------------------------
def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        text = ""
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n\n"

            if not text.strip():
                doc = fitz.open(filepath)
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img) + "\n\n"

        except Exception as e:
            return f"Error extracting PDF: {e}"

        return text.strip()

    elif ext in [".png", ".jpg", ".jpeg"]:
        try:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            return f"Error extracting image: {e}"

    elif ext == ".txt":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
            return text
        except Exception as e:
            return f"Error reading text file: {e}"

    else:
        return "Unsupported file format"


# ---------------------------
# Text Analysis Function
# ---------------------------
def analyze_text(text):
    if not text.strip():
        return {
            "sentiment": "neutral",
            "polarity": 0,
            "keywords": [],
            "suggestions": ["No meaningful text found to analyze."]
        }

    sentiment_scores = sia.polarity_scores(text)
    polarity = sentiment_scores["compound"]

    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    words = re.findall(r"\b\w+\b", text.lower())
    stopwords = {"the", "is", "and", "a", "to", "of", "in", "for", "on", "at", "with", "as", "by", "an"}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    top_keywords = [w for w, _ in Counter(keywords).most_common(5)]

    suggestions = []
    if sentiment == "negative":
        suggestions.append("This post has negative sentiment. Consider rephrasing positively.")
    if len(top_keywords) < 3:
        suggestions.append("Add more relevant hashtags or keywords to boost visibility.")
    if len(text.split()) < 30:
        suggestions.append("Longer posts often perform better. Consider adding more detail.")
    else:
        suggestions.append("Your content length looks good!")

    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "keywords": top_keywords,
        "suggestions": suggestions
    }


# ---------------------------
# File Upload Endpoint
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    extracted_text = extract_text_from_file(filepath)
    analysis = analyze_text(extracted_text)

    return jsonify({
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "content": extracted_text,
        "text": extracted_text,
        "analysis": analysis
    })


# ---------------------------
# Serve React Frontend
# ---------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# ---------------------------
# Run Flask
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
