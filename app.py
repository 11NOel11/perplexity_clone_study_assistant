import os
import requests
import streamlit as st
st.set_page_config(page_title="STUDY ASSISTANT", layout="wide")
import fitz  # PyMuPDF for PDF text extraction
import sympy as sp
from googleapiclient.discovery import build
from utils.pdf_handler import extract_text_from_pdf
from utils.google_search import google_search
from utils.math_solver import solve_equation
from utils.summarizer import summarize_text
from dotenv import load_dotenv

# Load API keys from .env file
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    st.error("❌ API Key or CSE ID is missing. Please check the .env file.")

# Function to handle PDF uploads and extract equations
def handle_pdf_and_solutions(pdf_file):
    extracted_text = extract_text_from_pdf(pdf_file)
    if not extracted_text:
        st.warning("No text extracted from the PDF.")
        return
    st.write("### Extracted Text from PDF:")
    st.write(extracted_text)
    
    equations = [line for line in extracted_text.split('\n') if '=' in line]
    if equations:
        st.write("### Solving Equations:")
        for eq in equations:
            st.write(f"Solving: {eq}")
            solution = solve_equation(eq)
            st.write(f"Solution: {solution}")

# Frontend navigation
def main():
    st.sidebar.image("assets/images/logo.png", use_container_width=True)
    st.sidebar.title('STUDY ASSISTANT')
    selection = st.sidebar.radio("Choose a page", ["Home", "Assignment Solver", "Create Short Notes"])
    
    if selection == "Home":
        st.title('Welcome to STUDY ASSISTANT')
        query = st.text_input('Enter a query or topic:')
        if query:
            results = google_search(query)
            if results:
                st.write("### Search Results:")
                for res in results:
                    st.markdown(f"### [{res['title']}]({res['link']})")
                    st.write(res['snippet'])
                summary = summarize_text(" ".join([r['snippet'] for r in results]))
                st.write("### Summary of Search Results:")
                st.write(summary)
    
    elif selection == "Assignment Solver":
        st.title('Assignment Solver')
        pdf_file = st.file_uploader("Upload your PDF assignment", type="pdf")
        if pdf_file:
            handle_pdf_and_solutions(pdf_file)
    
    elif selection == "Create Short Notes":
        st.title('Create Short Notes')
        topic = st.text_input('Enter a topic:')
        
        # NEW: Slider UI to adjust summary length
        min_summary_length = st.slider("Minimum Summary Length", min_value=10, max_value=200, value=50, step=10)
        max_summary_length = st.slider("Maximum Summary Length", min_value=100, max_value=500, value=300, step=50)

        if topic:
            results = google_search(topic)
            if results:
                for res in results:
                    st.markdown(f"### [{res['title']}]({res['link']})")
                    st.write(res['snippet'])
                
                # Pass dynamic values to summarization
                summary = summarize_text(" ".join([r['snippet'] for r in results]), max_length=max_summary_length, min_length=min_summary_length)
                st.write("### Summary of Topic:")
                st.write(summary)
    
if __name__ == '__main__':
    main()
