<h1 style="font-size:40px;"> Social Media Content Analyzer</h1>

<p>
A web-based tool that extracts text from PDFs and images, performs sentiment analysis, 
and highlights important keywords. It also provides a clean user interface with 
light/dark mode toggle for better readability.
</p>



<h2 style="font-size:28px;">🚀 Features</h2>

- Upload **PDF/Image** files and extract text.  
- Works with both digital and scanned PDFs (**OCR support**).  
- **Sentiment detection** (positive, neutral, negative) with polarity score.  
- Extracts **top keywords** and generates suggestions.  
- Light/Dark theme toggle with styled text box.  
- **User-friendly interface**.  



<h2 style="font-size:28px;">🛠️ Tools, Technologies & Libraries</h2>

<h3 style="font-size:22px;">Frontend</h3>
- ⚛️ React.js (UI development)  
- 🎨 CSS / Inline styles for theming  
- 🌗 Theme Toggle (Light/Dark Mode)  

<h3 style="font-size:22px;">Backend</h3>
- 🐍 Flask (Python web framework)  
- 🌍 Flask-CORS (cross-origin requests)  

<h3 style="font-size:22px;">Text Extraction & OCR</h3>
- 📄 PyMuPDF (fitz) – extract text from PDFs  
- 🔍 PyPDF2 – parse digital PDFs  
- 🖼 Pillow (PIL) – image handling  
- 🤖 PyTesseract – OCR for scanned PDFs  

<h3 style="font-size:22px;">Natural Language Processing (NLP)</h3>
- 🧠 NLTK (Natural Language Toolkit)  
- 📝 VADER SentimentIntensityAnalyzer  

---

<h2 style="font-size:28px;">⚡ Installation</h2>

1. Setup **Flask backend** with required libraries.  
2. Setup **React frontend** with `npm install`.  
3. Start Flask:  
   ```bash
   python app.py