# 🔮 Exam Oracle

**Exam Oracle** is an AI-powered Streamlit application that predicts *how* an instructor is likely to design exam questions — and *what kind* of questions students should expect.

By combining a structured quiz, instructor persona modeling, and optional past exam PDF analysis, Exam Oracle generates realistic, instructor-aligned exam questions using Large Language Models (LLMs).

---

## ✨ Features

- 🧠 **Instructor Persona Analysis**  
  Models the instructor as personas (e.g. *Klasikçi*, *Analitik*, *Tuzakçı*) based on quiz answers.

- 📋 **Exam Style Prediction**  
  Predicts exam format, question tendencies, and difficulty patterns.

- 📝 **AI-Generated Example Questions**  
  Generates realistic, exam-style questions aligned with:
  - instructor persona  
  - course context  
  - exam type & difficulty  

- 📎 **Past Exam PDF Support (Optional)**  
  Upload previous exam PDFs to help the AI mimic:
  - wording style  
  - question structure  
  - tone and length  

- 🔐 **Secure API Key Handling**  
  API keys are kept private and are never exposed to users.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend / Logic:** Python  
- **AI / LLM:** Gemma 3 4B – free tier
- **PDF Parsing:** PyPDF  
- **Environment Management:** python-dotenv  

---

## 🚀 How It Works

1. The user fills out a structured quiz about:
   - course type  
   - instructor habits  
   - exam style  
   - difficulty preferences  

2. The system:
   - calculates instructor persona scores  
   - determines primary & secondary personas  

3. (Optional) The user uploads past exam PDFs:
   - text is extracted  
   - style signals are injected into the prompt  

4. The LLM generates:
   - exam style analysis  
   - realistic example questions  
   - targeted study strategies  

