import os
import json
import pandas as pd
from openai import OpenAI
from helper_functions import llm
from dotenv import load_dotenv


def generate_mcq(user_message, num_questions=10):
    
    delimiter = "####"

    system_message = f"""
    You will be provided with a document. \
    The document will be enclosed in
    the pair of {delimiter}.

    Follow these rules:

    1. Ignore the texts related table of contents, empty sections, purely structural headings, and any content that does not contain facts.
    2. Extract facts only from meaningful paragraphs, descriptions, and business rules.
    3. Generate exactly {num_questions} questions.
    4. The questions can be of the following types:
        a. Multiple choice questions (MCQs) with 4 options (A, B, C, D).
        b. What is the correct answer based on the document with 4 options (A, B, C, D).
        c. Open-ended questions with a single correct answer.
    5. Each question should be clear, concise, and relevant to the content of the document.
    4. For each question, it shoul have the following details.
        a. Question no (1–10)
        b. Question text (clear, concise)
        c. Option A, Option B, Option C, Option D (randomized order)
        d. Correct Answer (single capital letter A–D)
        e. Reference (the original text from which the question was derived)
    5. Randomize the order of the questions.
    6. Randomize the order of the answer options for each question.
    8. Ensure your response contains only the JSON array, without any enclosing tags or delimiters.
    9. If are no relevant questions, output an empty list.
    10.Ensure your response contains only the list of dictionary objects or an empty list, \
        without any enclosing tags or delimiters.
            
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    mcq_str = llm.get_completion_by_messages(messages)
    print(mcq_str)
    mcq_questions_and_answers = json.loads(mcq_str)
    print(mcq_questions_and_answers)
    return mcq_questions_and_answers

def generate_open_ended_questions(user_message, num_questions=10):
    
    delimiter = "####"

    system_message = f"""
    You will be provided with a document. \
    The document will be enclosed in
    the pair of {delimiter}.

    Follow these rules:

    1. Ignore the texts related table of contents, empty sections, purely structural headings, and any content that does not contain facts.
    2. Extract facts only from meaningful paragraphs, descriptions, and business rules.
    3. Generate exactly {num_questions} open-ended questions.
    5. Each question should be clear, concise, and relevant to the content of the document.
    4. For each question, it shoul have the following details.
        a. Question no (1–10)
        b. Question text (clear, concise)
        d. Correct Answer 
        e. Reference (the original text from which the question was derived)
    5. Randomize the order of the questions.
    6. Randomize the order of the answer options for each question.
    8. Ensure your response contains only the JSON array, without any enclosing tags or delimiters.
    9. If are no relevant questions, output an empty list.
    10.Ensure your response contains only the list of dictionary objects or an empty list, \
        without any enclosing tags or delimiters.
            
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    open_str = llm.get_completion_by_messages(messages)
    print(open_str)
    open_questions_and_answers = json.loads(open_str)
    print(open_questions_and_answers)
    return open_questions_and_answers

def clean_text(user_message):
    
    delimiter = "####"

    system_message = f"""
    You will be provided with a information extracted from document. The document contains title, headings, detail content, etc\
    The document will be enclosed in
    the pair of {delimiter}.

    Follow these rules:

    1. Ignore the texts related table of contents, empty sections, purely structural headings, and any content that does not contain facts.
    2. Ignore those sections which are marked as Not applicable, Not relevant, or Not applicable.
            
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    open_str = llm.get_completion_by_messages(messages)
    print(open_str)
    return open_str



def generate_questions(user_input, num_questions=10):
    delimiter = "```"

    user_output = clean_text(user_input)
    print(user_output)
    #return user_output
    # Process 1: If Courses are found, look them up
    questions_and_answers_mcq = generate_mcq(user_output)
    print(questions_and_answers_mcq)
    questions_and_answers_freeText = generate_open_ended_questions(user_output)
    return questions_and_answers_mcq, questions_and_answers_freeText

