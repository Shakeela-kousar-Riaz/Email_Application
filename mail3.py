import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langdetect import detect
from email_validator import validate_email, EmailNotValidError
from translate import Translator
import random
import string
import pandas as pd

# --- Helper Functions ---
def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def translate_content(content, target_language):
    translator = Translator(to_lang=target_language)
    try:
        return translator.translate(content)
    except Exception:
        return "Translation Error"

def send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, message):
    try:
        # Setting up SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        # Creating email
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Sending email
        server.send_message(msg)
        server.quit()
        return "Email Sent Successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

# --- Streamlit App ---
st.set_page_config(page_title="Email Management App", layout="wide")

# Sidebar for configurations
st.sidebar.title("Email Management")
smtp_server = st.sidebar.text_input("SMTP Server", "smtp.example.com")
smtp_port = st.sidebar.number_input("SMTP Port", min_value=1, value=587, step=1)
smtp_user = st.sidebar.text_input("SMTP Email Address", "your-email@example.com")
smtp_password = st.sidebar.text_input("SMTP Password", type="password")

st.sidebar.subheader("Email Options")
email_count = st.sidebar.slider("Number of Random Emails", min_value=1, max_value=50, value=5)
target_language = st.sidebar.selectbox("Target Language for Translation", ["English", "es", "French", "spanish", "ur"])

# Main Section
st.title("📧 Email Management Dashboard")

# 1. Generate Random Emails
st.subheader("Step 1: Generate Random Emails")
if st.button("Generate Emails"):
    emails = [generate_random_email() for _ in range(email_count)]
    st.write("Generated Emails:")
    st.table(emails)

# 2. Validate Emails
st.subheader("Step 2: Validate Emails")
email_to_validate = st.text_input("Enter Email to Validate")
if st.button("Validate Email"):
    if validate_email_address(email_to_validate):
        st.success("The email address is valid!")
    else:
        st.error("The email address is invalid!")

# 3. Translate Email Content
st.subheader("Step 3: Translate Email Content")
email_content = st.text_area("Enter Email Content for Translation", height=150)
if st.button("Translate Content"):
    detected_language = detect(email_content)
    translated_text = translate_content(email_content, target_language)
    st.write(f"Detected Language: {detected_language}")
    st.write(f"Translated Content ({target_language}):")
    st.text_area("Translated Content", translated_text, height=150)

# 4. Send Email
st.subheader("Step 4: Send Email")
to_email = st.text_input("Recipient Email Address")
subject = st.text_input("Email Subject")
message = st.text_area("Email Message", height=200)
if st.button("Send Email"):
    if validate_email_address(to_email):
        result = send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, message)
        if "Successfully" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Invalid recipient email address!")

# 5. Email Analytics (Placeholder)
st.subheader("Step 5: Email Analytics (Coming Soon)")
st.write("This section will include analytics like open rates, click rates, and more.")

