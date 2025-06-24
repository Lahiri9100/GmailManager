
# 📬 Gmail Manager AI

**Gmail Manager AI** is a Streamlit-based app that helps users analyze emails by extracting key details like deadlines, tags, suggested replies, and summaries using basic NLP techniques.

---

## 🚀 Features

- 🧠 Extracts important **dates/deadlines**
- 🏷️ Automatically tags emails (e.g., Project, Meeting, Deadline)
- 💬 Suggests short, context-aware auto-replies
- 📝 Summarizes the email using **Latent Semantic Analysis (LSA)**
- 🗓️ Saves the extracted data to a CSV calendar
- 📊 Built-in calendar view to manage tasks

---

## 🧪 Tech Stack

- **Frontend**: Streamlit
- **NLP**: Sumy (LSA), NLTK, Regex
- **Storage**: CSV file (`calendar.csv`)
- **Other**: Python standard libraries

---

## ⚙️ Requirements

Install all required packages with:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install streamlit pandas ics streamlit-calendar sumy nltk
```

Also, run the following once in your script to avoid NLTK errors:

```python
import nltk
nltk.download('punkt')
```

---

## 🧾 How to Use

1. Run the app with:
```bash
streamlit run Gmail_Manager.py
```

2. Paste your email in the text box.
3. Click "🧠 Process Email" to extract insights.
4. View summary, tags, reply suggestion, and see it saved to calendar.

---

## 📂 File Structure

- `Gmail_Manager.py` – Main application logic
- `calendar.csv` – Stores your processed email details
- `requirements.txt` – All Python dependencies

---

## 🛠 Dev Container Support

Includes a `.devcontainer.json` file for running in VSCode + GitHub Codespaces with preinstalled Python environment.

---

## 👤 Author

Developed for educational and productivity enhancement purposes.
