import streamlit as st
import pandas as pd
import re
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from auth import create_users_table, register_user, login_user
from database import (
    init_db,
    save_email,
    load_emails,
    load_active_deadlines
)

# ---------------- NLTK SETUP ----------------

nltk_packages = ["punkt", "punkt_tab"]

for pkg in nltk_packages:
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg)

# ---------------- DATABASE INIT ----------------

init_db()
create_users_table()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
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

# ---------------- AUTH SECTION ----------------

if not st.session_state.logged_in:

    st.title("🔐 Gmail Manager AI Login")

    auth_mode = st.sidebar.selectbox(
        "Choose Option",
        ["Login", "Register"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if auth_mode == "Register":

        if st.button("Create Account"):

            if username and password:

                success = register_user(
                    username,
                    password
                )

                if success:
                    st.success("✅ Account created successfully.")

                else:
                    st.error("❌ Username already exists.")

            else:
                st.warning("Please fill all fields.")

    else:

        if st.button("Login"):

            if login_user(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:
                st.error("❌ Invalid username or password.")

# ---------------- MAIN APPLICATION ----------------

else:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    st.title("📩 Gmail Manager AI")

    st.markdown(
        """
    This AI assistant reads your emails,
    finds deadlines, tags, summaries,
    replies, and stores analysis history locally.
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

            save_email(
                st.session_state.username,
                deadline,
                ", ".join(tags),
                reply,
                summary
            )

            st.success(
                "✅ Email analyzed and stored successfully."
            )

            st.write("**📅 Deadline:**", deadline)

            st.write("**🏷️ Tags:**", ", ".join(tags))

            st.write("**💬 Suggested Reply:**", reply)

            st.write("**📋 Summary:**")

            st.info(summary)

        # ---------------- ACTIVE DEADLINES ----------------

    st.subheader("📌 Active Deadlines")

    active_deadlines = load_active_deadlines(
        st.session_state.username
    )

    if active_deadlines:

        active_df = pd.DataFrame(
            active_deadlines,
            columns=[
                "Deadline",
                "Tags",
                "Summary",
                "Created At"
            ]
        )

        active_df["Summary"] = (
            active_df["Summary"]
            .astype(str)
            .str[:80] + "..."
        )

        st.dataframe(
            active_df,
            width="stretch"
        )

    else:

        st.info("No active deadlines.")

    # ---------------- FULL HISTORY ----------------

    with st.expander("📁 Full Analysis History"):

        history = load_emails(
            st.session_state.username
        )

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

            history_df["Summary"] = (
                history_df["Summary"]
                .astype(str)
                .str[:80] + "..."
            )

            st.dataframe(
                history_df,
                width="stretch"
            )

        else:

            st.info("No history available yet.")