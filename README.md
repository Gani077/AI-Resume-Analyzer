# 🤖 AI Resume Analyzer

An intelligent web application that analyzes resumes against job descriptions and provides a **match score, detected skills, missing skills, and personalized recommendations**.

---

## 🚀 Live Demo
👉 https://your-railway-link.up.railway.app  

---

## 📌 Features

- 📄 Upload Resume (PDF / DOCX)
- 🧠 Domain-based skill detection (Data Science, Web Dev, AI/ML, etc.)
- 📊 Match Score calculation
- ✅ Detected Skills extraction
- ❌ Missing Skills identification
- 💡 Smart Recommendations
- 🌙 Dark / Light mode toggle
- 📱 Responsive UI (Mobile + Desktop)
- ⚡ Fast backend using Flask

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python (Flask)
- pdfplumber
- python-docx
- scikit-learn
- spaCy

### Deployment
- Railway
- GitHub

---

## 🧠 How It Works

1. User uploads resume
2. User enters job description
3. System detects domain (Data Science / Web / AI / etc.)
4. Matches resume with predefined skill database
5. Generates:
   - Match Score
   - Detected Skills
   - Missing Skills
   - Recommendations

---

## 📂 Project Structure
```
AI Resume Analyzer/
│
├── static/
│  ├── imgs/
│     ├── icon.png
│  │-- style.css
│  │-- style_old.css         
│
├── templates/             
│   │-- index.html  
│
│--analyzer.py
│--app.py
│--skill_extractor.py
│--requirements.txt
│--Procfile
│--runtime.txt
│     
├── README.md         
```


---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Gani077/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally
```bash
python app.py
```

### 4. Open
```bash
http://127.0.0.1:5000
```
---

## 🚀 Future Improvements

- ATS breakdown
- Graph-based analysis
- Resume Improvement suggestions
- User login system
- Download Report

---

## 👨‍💻 Author

### Ganesh(SVSG)

🔗Github: 
```bash
https://github.com/Gani077
```

---

## ⭐ Support
If you like this project give it a ⭐ on Github!
💬 Feel free to fork, contribute, and improve it.
