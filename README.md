<p align="center">
  <img src="logo.png" width="150"/>
</p>

> Turn documents into structured intelligence.

# 🧠 Literature Brain

> A local AI-powered research assistant that turns documents into structured, searchable knowledge.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Ollama](https://img.shields.io/badge/LLM-Ollama-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🚀 Features

- 📄 Process PDFs, DOCX, XLSX, PPTX
- 🧠 Extract structured insights using local LLMs
- 🔍 Query across your entire document library
- 💬 Chat-style interface (Streamlit)
- ⚡ Fully local — no cloud required

---

## 🖼️ Demo

### App Interface
![App Screenshot](screenshots/app.png)

### Example Query
![Demo](screenshots/demo.gif)

---

## 🧩 How It Works


data/ → process_paper.py → Ollama (LLaMA 3) → outputs/*.json → brain.py → Streamlit UI


---

## ⚙️ Setup

### 1. Install dependencies

pip install -r requirements.txt


### 2. Install Ollama
https://ollama.com

### 3. Pull model

ollama pull llama3


### 4. Run the app

python -m streamlit run app.py


---

## 📁 Project Structure


vibe-coding/<br>
├── app.py # Streamlit UI<br>
├── brain.py # Query engine<br>
├── process_paper.py # Data ingestion pipeline<br>
├── outputs/ # Structured JSON<br>
├── data/ # Source documents


---

## 🧠 Future Improvements

- 🔎 Semantic search (embeddings)
- 📊 Tag filtering UI
- 📄 Document viewer
- ⚡ Streaming responses
- 🧾 Inline citations

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

---

## 📜 License

MIT
