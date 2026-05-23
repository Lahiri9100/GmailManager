# 📩 Gmail Manager AI

An AI-powered email productivity assistant built using Python, Streamlit, NLP, and SQLite.

This project analyzes unstructured email content and performs intelligent processing such as:
- email summarization
- deadline extraction
- smart tagging
- auto-reply generation
- active deadline tracking
- user-specific analysis history

The system is designed as a **privacy-focused local prototype** without direct Gmail account integration.

---

# 🚀 Features

## 🔐 User Authentication
- User registration and login system
- Password hashing using bcrypt
- User-specific email history storage

---

## 🧠 NLP-Based Email Processing
The application performs intelligent processing on pasted email content using NLP techniques.

### Supported capabilities:
- Email summarization
- Deadline extraction
- Smart categorization/tagging
- Suggested auto replies

---

## 📌 Active Deadlines Dashboard
- Automatically tracks upcoming deadlines
- Filters expired deadlines dynamically
- Supports multiple date formats

### Supported Date Formats
- June 5th
- 5 June 2026
- Jun 5
- 5 Jun
- May 28th, 2026

---

## 📁 Full Analysis History
- Stores processed email history
- User-specific persistent storage
- SQLite-based local database

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend logic |
| Streamlit | Web application UI |
| SQLite | Local database storage |
| NLTK | NLP preprocessing |
| Sumy | Text summarization |
| Pandas | Data handling |
| Regex | Deadline extraction |

---

# 🧩 Project Architecture

```text
User Input
     ↓
NLP Processing Layer
     ↓
Summarization + Tagging + Deadline Extraction
     ↓
SQLite Database Storage
     ↓
Active Deadline Dashboard + Analysis History