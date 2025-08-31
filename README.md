<h1 style="font-size:40px;"> Social Media Content Analyzer</h1>

<p>
A web-based tool that extracts text from PDFs and images, performs sentiment analysis, 
and highlights important keywords. It also provides a clean user interface with 
light/dark mode toggle for better readability.
</p>



<h2 style="font-size:28px;">🚀 Features</h2>

- Upload **PDF/Image** files and extract text.  <br> 
- Works with both digital and scanned PDFs (**OCR support**).  <br> 
- **Sentiment detection** (positive, neutral, negative) with polarity score.  <br> 
- Extracts **top keywords** and generates suggestions.  <br> 
- Light/Dark theme toggle with styled text box.  <br> 
- **User-friendly interface**.  <br> 



<h2 style="font-size:28px;">🛠️ Tools, Technologies & Libraries</h2>

<h3 style="font-size:22px;">Frontend</h3>
- ⚛️ React.js (UI development) <br> 
- 🎨 CSS / Inline styles for theming  <br> 
- 🌗 Theme Toggle (Light/Dark Mode)  <br> 

<h3 style="font-size:22px;">Backend</h3>
- 🐍 Flask (Python web framework)  <br> 
- 🌍 Flask-CORS (cross-origin requests)  <br> 

<h3 style="font-size:22px;">Text Extraction & OCR</h3> 
- 📄 PyMuPDF (fitz) – extract text from PDFs  <br> 
- 🔍 PyPDF2 – parse digital PDFs  <br> 
- 🖼 Pillow (PIL) – image handling  <br> 
- 🤖 PyTesseract – OCR for scanned PDFs<br>   

<h3 style="font-size:22px;">Natural Language Processing (NLP)</h3>
- 🧠 NLTK (Natural Language Toolkit)  <br> 
- 📝 VADER SentimentIntensityAnalyzer <br>  

---

<h2 style="font-size:28px;">⚡ Installation</h2>

1. Setup **Flask backend** with required libraries.  
2. Setup **React frontend** with `npm install`.  
3. Start Flask:  
   ```bash
   python app.py
