import streamlit as st
import pandas as pd
import re
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')

def generate_summary(text):
    try:
        cleaned = clean_email_text(text)
        parser = PlaintextParser.from_string(cleaned, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 2)
        summary = " ".join(str(sentence) for sentence in summary_sentences)
        return summary if summary else "No clear summary could be generated."
    except Exception as e:
        return f"⚠️ Error while summarizing locally: {e}"

# --- Helper Functions ---
def extract_date(text):
    patterns = [
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b',
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?\b'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group()
    return "No deadline found"

def tag_email(text):
    tags = []
    if "project" in text.lower(): tags.append("Project")
    if "submit" in text.lower(): tags.append("Deadline")
    if "meeting" in text.lower(): tags.append("Meeting")
    if "reminder" in text.lower(): tags.append("Reminder")
    return tags or ["General"]

def generate_reply(text):
    if "submit" in text.lower():
        return "Thank you! I’ll submit it by the deadline."
    elif "meeting" in text.lower():
        return "Noted. I’ll be there."
    else:
        return "Got it. Thank you!"

def clean_email_text(text):
    text = re.sub(r"On\\s.+?wrote:.*", "", text, flags=re.DOTALL)
    text = re.sub(r"--\\s*\\n.*", "", text)
    return text.strip()


# --- Streamlit UI ---
st.title("\U0001F4E9 Gmail Manager AI")
st.markdown("This AI assistant reads your emails, finds deadlines, tags, summaries, replies, and saves them to your calendar.")

email_input = st.text_area("\U0001F4EC Paste your email here:", height=200)

if st.button("\U0001F9E0 Process Email"):
    if email_input.strip() == "":
        st.warning("Please paste an email first.")
    else:
        deadline = extract_date(email_input)
        tags = tag_email(email_input)
        reply = generate_reply(email_input)
        summary = generate_summary(email_input)

        calendar_entry = {
            "Date/Deadline": deadline,
            "Tags": ", ".join(tags),
            "Auto-Reply": reply
        }

        try:
            df = pd.read_csv("calendar.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=calendar_entry.keys())

        df = pd.concat([df, pd.DataFrame([calendar_entry])], ignore_index=True)
        df.to_csv("calendar.csv", index=False)

        st.success("\u2705 Email analyzed and added to calendar.")
        st.write("**\U0001F4C5 Deadline:**", deadline)
        st.write("**\U0001F3F7️ Tags:**", ", ".join(tags))
        st.write("**\U0001F4AC Suggested Reply:**", reply)
        st.write("**\U0001F4CB Summary:**")
        st.info(summary)

        with st.expander("\U0001F4C1 View Calendar"):
            st.dataframe(df)
