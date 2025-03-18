import streamlit as st
import time
import plotly.graph_objects as go
from PIL import Image

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Header & Footer Templates
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# Streamlit App Content
st.title("📘 Welcome to Study Assistant")
st.write("Navigate through the options in the sidebar to explore features.")

# Parallax Section
st.markdown('<div class="parallax"></div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to:", ["Home", "Assignment Solver", "Create Short Notes"])

if selection == "Home":
    st.subheader("🔍 Search JEE Topics")
    query = st.text_input("Enter a topic:")
    if query:
        st.write("Fetching results...")
        time.sleep(1)
        # Placeholder for search results
        st.success("Results will be shown here!")
    
    # Interactive Graph Example
    fig = go.Figure(data=[go.Bar(x=["Topic A", "Topic B", "Topic C"], y=[10, 15, 7])])
    fig.update_layout(title='Topic Relevance', xaxis_title='Topics', yaxis_title='Score')
    st.plotly_chart(fig)

elif selection == "Assignment Solver":
    st.subheader("📄 Upload and Solve Assignments")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF uploaded successfully!")
        with st.spinner('Processing your PDF...'):
            time.sleep(2)
        st.write("Solutions will be displayed here!")

elif selection == "Create Short Notes":
    st.subheader("📝 Generate Short Notes")
    topic = st.text_input("Enter a topic:")
    if topic:
        st.write("Generating notes...")
        time.sleep(1)
        st.success("Short notes will be shown here!")

# Load Footer
with open("templates/footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
