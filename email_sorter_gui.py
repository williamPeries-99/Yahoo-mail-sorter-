import streamlit as st
import json
import os
from email_sorter_core import process_emails

CONFIG_FILE = "config.json"

st.set_page_config(page_title="Yahoo Email Sorter", layout="centered")
st.title("📥 Yahoo Email Sorter")

# Load config if exists
config = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

# Input fields
email_input = st.text_input("Yahoo Email", value=config.get("email", ""))
password_input = st.text_input("App Password", type="password", value=config.get("password", ""))
source_folder = st.text_input("Source Folder", value=config.get("source_folder", "INBOX"))
destination_folder = st.text_input("Destination Folder", value=config.get("destination_folder", "Important"))

important_senders = st.text_area(
    "Important Senders (one per line)",
    value="\n".join(config.get("important_senders", []))
)

# Save config
if st.button("💾 Save Settings"):
    config = {
        "email": email_input,
        "password": password_input,
        "source_folder": source_folder,
        "destination_folder": destination_folder,
        "important_senders": [s.strip().lower() for s in important_senders.splitlines() if s.strip()]
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    st.success("Settings saved!")

# Run sorter
if st.button("▶️ Run Sorter Now"):
    with st.spinner("Running sorter..."):
        process_emails()
    st.success("Email sorting complete. Check the log file for details.")
