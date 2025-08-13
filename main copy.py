# Set up and run this Streamlit App
import streamlit as st
import docx
import random
import re
import json

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

# ===== Function to generate questions =====
def generate_questions(text, num_questions=10):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 15]
    questions = []
    
    # Pick unique sentences for questions
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    
    for i, sentence in enumerate(selected_sentences, start=1):
        correct_answer = sentence
        # Create wrong options by picking other sentences
        wrong_answers = random.sample([s for s in sentences if s != correct_answer], 3)
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Store in required JSON format
        questions.append({
            "Question no": i,
            "Question": f"What is correct based on the document? ({i})",
            "Option A": options[0],
            "Option B": options[1],
            "Option C": options[2],
            "Option D": options[3],
            "Correct Answer": chr(65 + options.index(correct_answer))  # 65 = 'A'
        })
    
    random.shuffle(questions)  # Shuffle question order
    return questions

# ===== Streamlit UI =====
st.title("📄 Quizzer Bot - Word Document to Random MCQs")

uploaded_file = st.file_uploader("Upload a Word document (.docx)", type=["docx"])

if uploaded_file:
    raw_text = read_word(uploaded_file)
    cleaned_text = clean_text(raw_text)
    
    st.subheader("📑 Extracted Text (Cleaned)")
    st.text_area("Document Content", cleaned_text, height=300)
    
    if st.button("Generate Quiz"):
        quiz_data = generate_questions(cleaned_text, num_questions=10)
        st.subheader("📝 Generated Quiz (JSON)")
        st.code(json.dumps(quiz_data, indent=2), language="json")