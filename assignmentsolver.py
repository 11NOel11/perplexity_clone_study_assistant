import streamlit as st
from utils.pdf_handler import extract_text_from_pdf
from utils.google_search import google_search
from utils.math_solver import solve_equation
import os

def solve_assignment(pdf_file):
    """Processes an uploaded PDF, extracts text, and solves relevant questions."""
    extracted_text = extract_text_from_pdf(pdf_file)
    if not extracted_text:
        return "No text extracted from the PDF."
    
    solutions = []
    for line in extracted_text.split('\n'):
        if "=" in line:
            solution = solve_equation(line)
        else:
            solution = google_search(line)
        solutions.append(f"{line}: {solution}")
    
    return "\n".join(solutions)

# Streamlit UI
st.set_page_config(page_title="Assignment Solver", layout="wide")
st.title("📘 Assignment Solver")
st.write("Upload a PDF to extract text, search Google, or solve math equations!")

uploaded_file = st.file_uploader("Upload your assignment PDF", type=["pdf"])
if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    solution = solve_assignment("temp.pdf")
    os.remove("temp.pdf")  # Clean up temp file
    st.subheader("Solutions:")
    st.write(solution)
