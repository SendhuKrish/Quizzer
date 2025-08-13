# Set up and run this Streamlit App
import streamlit as st
import docx
import random
import re
import json
from logics.Quiz_generator import generate_questions

import sys
sys.dont_write_bytecode = True

# ===== Function to read Word document =====
def read_word(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)
    return "\n".join(full_text)

# ===== Function to clean text (remove Table of Contents, empty sections) =====
def clean_text(text):
    lines = text.split("\n")
    cleaned = []
    toc_pattern = re.compile(r"^(\d+(\.\d+)*)?\s*(Contents|Table of Contents)", re.IGNORECASE)
    empty_pattern = re.compile(r"^\s*$")
    
    for line in lines:
        if toc_pattern.search(line):
            continue
        if empty_pattern.match(line):
            continue
        # Remove page numbers in TOC-like entries (e.g., "...  4")
        if re.search(r"\.{3,}\s*\d+$", line):
            continue
        cleaned.append(line)
    
    return "\n".join(cleaned)


# ===== Streamlit UI =====
st.title("📄 Quizzer Bot - Word Document to Random MCQs")

uploaded_file = st.file_uploader("Upload a Word document (.docx)", type=["docx"])

if uploaded_file:
    raw_text = read_word(uploaded_file)
    cleaned_text = clean_text(raw_text)
    
    st.subheader("📑 Extracted Text (Cleaned)")
    st.text_area("Document Content", cleaned_text, height=300)
    
    if st.button("Generate Quiz"):
        quiz_data_mcq, quiz_data_freetext = generate_questions(cleaned_text, num_questions=10)
        st.subheader("📝 Generated Quiz (JSON)")
        st.code(json.dumps(quiz_data_mcq, indent=2), language="json")
        st.code(json.dumps(quiz_data_freetext, indent=2), language="json")