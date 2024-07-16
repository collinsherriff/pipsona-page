import streamlit as st
import pandas as pd
import numpy as np
import time

if "loading_done" not in st.session_state:
    st.session_state.loading_done = False

if not st.session_state.loading_done:
    # Display loading animation
    st.markdown("""
        <style>
            @keyframes loader {
                0% { width: 0%; }
                100% { width: 100%; }
            }
            .loader {
                width: 100%;
                background: #f3f3f3;
                border: 1px solid #ccc;
                border-radius: 5px;
                overflow: hidden;
            }
            .loader-bar {
                height: 30px;
                background: linear-gradient(90deg, #4caf50, #81c784);
                animation: loader 1s linear forwards;
            }
        </style>
        <div class="loader">
            <div class="loader-bar"></div>
        </div>
        <br/>
        <div style="text-align:center">Loading PiP Personality Test... Please wait</div>
    """, unsafe_allow_html=True)
    
    time.sleep(2)  # Simulate a delay for loading
    st.session_state.loading_done = True
    st.experimental_rerun()

# Define the OCEAN scores for each persona
persona_scores = {
    "Patient Planner": [3, 5, 4, 2, 1],
    "The Bandwagoner": [4, 4, 3, 2, 3],
    "The Overtrader": [3, 3, 4, 4, 5],
    "PVP Player": [2, 2, 4, 1, 3],
    "Bet and Forgetter": [5, 3, 4, 4, 2],
    "Volatility Seeker": [4, 2, 5, 3, 4]
}

def calculate_percentage_match(ocean_score, persona_scores):
    ocean_score = np.array([min(5, max(1, score)) for score in ocean_score])
    distances = {persona: np.linalg.norm(ocean_score - np.array(scores)) for persona, scores in persona_scores.items()}
    inverse_distances = {persona: (1 / distance if distance != 0 else float('inf')) for persona, distance in distances.items()}
    total_inverse_distance = sum(inverse_distances.values())
    percentage_matches = {persona: (inverse_distance / total_inverse_distance) * 100 for persona, inverse_distance in inverse_distances.items()}
    return percentage_matches

# Load questions and options from CSV
def load_questions_from_csv(csv_path):
    df = pd.read_csv(csv_path, header=None)
    questions = []
    i = 0
    while i < len(df):
        question = df.iloc[i, 0]
        options = df.iloc[i+1:i+6, 0].tolist()
        questions.append((question, options))
        i += 6
    return questions

# Assuming the CSV file is named 'questions.csv' and has the format specified
questions = load_questions_from_csv('questions.csv')

st.set_page_config(layout="wide", page_title="PiP Personality Test", page_icon=":coin:")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        body {
            font-family: 'Space Mono', monospace;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'VT323', monospace;
            font-weight: 400;
            color: white;
        }

        .question {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("logopixel2.png", use_column_width=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select section", ["PiP Personality Quiz", "Submit a Coinfessions"])
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Page navigation
if "page" not in st.session_state:
    st.session_state.page = 0

def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# Quiz pages
def welcome_page():
    st.title("Welcome to the OCEAN Personality Quiz")
    if st.button("Start Quiz"):
        next_page()

def question_page(question, options, question_index):
    st.markdown(f'<p class="question">Question {question_index + 1}: {question}</p>', unsafe_allow_html=True)
    answer = st.radio("", options, key=f"q{question_index}")
    if st.button("Next"):
        st.session_state[f"answer_{question_index}"] = options.index(answer) + 1
        next_page()
    if question_index > 0 and st.button("Previous"):
        prev_page()

def result_page():
    st.title("Your Results")
    st.image('output.png', use_column_width=True)
    answers = [st.session_state[f"answer_{i}"] for i in range(len(questions))]
    percentage_matches = calculate_percentage_match(answers, persona_scores)
    st.write("Your OCEAN score is:", answers)
    st.header("Your percentage match with each persona is:")
    for persona, percentage in percentage_matches.items():
        st.header(f"{persona}: {percentage:.2f}%")
    # if st.button("See Personalised Card"):
        # st.image(f"{persona}.png", use_column_width=True #if we use custom cards
    if st.button("Restart Quiz"):
        st.session_state.page = 0
        for i in range(len(questions)):
            del st.session_state[f"answer_{i}"]

# Render pages
if app_mode == "PiP Personality Quiz":
    if st.session_state.page == 0:
        welcome_page()
    elif 1 <= st.session_state.page <= len(questions):
        question_index = st.session_state.page - 1
        question, options = questions[question_index]
        question_page(question, options, question_index)
    else:
        result_page()
elif app_mode == "Submit a Coinfessions":
    st.title("Submit a Coinfession")
    coinfession_text = st.text_area("Enter your coinfession here:")
    if st.button("Submit Coinfession"):
        st.write("Thank you for your submission!")
        # Here, you could add code to handle the coinfession submission, such as saving it to a database or sending it via email.
