📬 Gmail Manager AI – Smart Email Summarizer & Calendar Assistant

Gmail Manager AI is a smart Streamlit app that reads emails, extracts deadlines, suggests replies, tags messages, and generates NLP-based summaries. Designed for professionals and students, it helps manage your inbox by converting unstructured emails into structured calendar entries.

---

🚀 Features

* ✍️ Paste email text directly into the app
* 📅 Deadline extractor using regex patterns
* 🏷️ Tag generator (Project, Meeting, Deadline, etc.)
* 💬 Auto-reply suggestions based on email content
* 🧠 NLP-based summarization (using Sumy + NLTK)
* 📊 Calendar-style table saved to `calendar.csv`
* 📂 View your scheduled entries inside the app

---

📁 File Structure

```
gmail-manager/
├── gmail_manager.py             # Main Streamlit application
├── requirements.txt             # Project dependencies
├── devcontainer.json            # VSCode DevContainer config
├── calendar.csv                 # Generated calendar entries (auto-created)
├── README.md                    # Project overview (this file)
```

---

🧪 Example Use

1. Paste your email into the app
2. Click “🧠 Process Email”
3. See:
   * 📅 Extracted deadline
   * 🏷️ Generated tags
   * 💬 Suggested reply
   * 🧠 AI-generated summary
   * 📊 Calendar entry table

---

🎓 Sample Use Case

Gmail Manager AI can help:

* Students keep track of assignment deadlines
* Professionals organize meeting requests
* Anyone who receives long emails quickly get summaries and calendar reminders

---

👨‍💻 Author

* N. Lahiri
  
---

📜 License

This project is intended for personal productivity and demo purposes. For production, email authentication, Gmail API integration, and encryption should be considered.
