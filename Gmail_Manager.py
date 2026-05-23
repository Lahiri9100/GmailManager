import streamlit as st
import pandas as pd
import re
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

from database import init_db, save_email, load_emails

# ---------------- NLTK SETUP ----------------

nltk_packages = ["punkt", "punkt_tab"]

for pkg in nltk_packages:
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg)

# ---------------- DATABASE INIT ----------------

init_db()

# ---------------- NLP FUNCTIONS ----------------

def clean_email_text(text):
    text = re.sub(r"On\\s.+?wrote:.*", "", text, flags=re.DOTALL)
    text = re.sub(r"--\\s*\\n.*", "", text)
    return text.strip()

def generate_summary(text):
    try:
        cleaned = clean_email_text(text)

        parser = PlaintextParser.from_string(
            cleaned,
            Tokenizer("english")
        )

        summarizer = LsaSummarizer()

        summary_sentences = summarizer(parser.document, 2)

        summary = " ".join(
            str(sentence)
            for sentence in summary_sentences
        )

        return summary if summary else "No clear summary could be generated."

    except Exception as e:
        return f"⚠️ Error while summarizing locally: {e}"

# ---------------- HELPER FUNCTIONS ----------------

def extract_date(text):

    patterns = [
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b',

        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?\b'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return "No deadline found"

def tag_email(text):

    tags = []

    if "project" in text.lower():
        tags.append("Project")

    if "submit" in text.lower():
        tags.append("Deadline")

    if "meeting" in text.lower():
        tags.append("Meeting")

    if "reminder" in text.lower():
        tags.append("Reminder")

    return tags or ["General"]

def generate_reply(text):

    if "submit" in text.lower():
        return "Thank you! I’ll submit it by the deadline."

    elif "meeting" in text.lower():
        return "Noted. I’ll be there."

    else:
        return "Got it. Thank you!"

# ---------------- STREAMLIT UI ----------------

st.title("📩 Gmail Manager AI")

st.markdown(
    """
This AI assistant reads your emails, finds deadlines,
tags, summaries, replies, and stores analysis history locally.
"""
)

email_input = st.text_area(
    "📬 Paste your email here:",
    height=200
)

if st.button("🧠 Process Email"):

    if email_input.strip() == "":
        st.warning("Please paste an email first.")

    else:

        deadline = extract_date(email_input)

        tags = tag_email(email_input)

        reply = generate_reply(email_input)

        summary = generate_summary(email_input)

        # -------- SAVE TO SQLITE DATABASE --------

        save_email(
            deadline,
            ", ".join(tags),
            reply,
            summary
        )

        # -------- OUTPUT --------

        st.success("✅ Email analyzed and stored successfully.")

        st.write("**📅 Deadline:**", deadline)

        st.write("**🏷️ Tags:**", ", ".join(tags))

        st.write("**💬 Suggested Reply:**", reply)

        st.write("**📋 Summary:**")

        st.info(summary)

# ---------------- HISTORY SECTION ----------------

with st.expander("📁 View Analysis History"):

    history = load_emails()

    if history:

        history_df = pd.DataFrame(
            history,
            columns=[
                "Deadline",
                "Tags",
                "Suggested Reply",
                "Summary",
                "Created At"
            ]
        )
        history_df["Summary"] = history_df["Summary"].str[:80] + "..."
        st.dataframe(
            history_df,
            width="stretch"
        )

    else:
        st.info("No history available yet.")