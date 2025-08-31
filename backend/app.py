from flask import Flask, request, jsonify
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


nltk.download("vader_lexicon")


sia = SentimentIntensityAnalyzer()


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------------------
# Text Extraction
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
# Text Analysis (with VADER)
# ---------------------------
def analyze_text(text):
    """Perform sentiment analysis + keyword frequency + suggestions"""
    if not text.strip():
        return {
            "sentiment": "neutral",
            "polarity": 0,
            "keywords": [],
            "suggestions": ["No meaningful text found to analyze."]
        }

    # Use VADER for sentiment analysis
    sentiment_scores = sia.polarity_scores(text)
    polarity = sentiment_scores["compound"]

    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Simple keyword extraction
    words = re.findall(r"\b\w+\b", text.lower())
    stopwords = {"the", "is", "and", "a", "to", "of", "in", "for", "on", "at", "with", "as", "by", "an"}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    top_keywords = [w for w, _ in Counter(keywords).most_common(5)]

    # Suggestions
    suggestions = []
    if sentiment == "negative":
        suggestions.append("This post has negative sentiment. Consider rephrasing in a more positive or supportive tone.")
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
# Upload Endpoint
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


if __name__ == "__main__":
    app.run(debug=True)
