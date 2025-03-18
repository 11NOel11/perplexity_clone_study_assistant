import requests
import streamlit as st
from googleapiclient.discovery import build
from utils.summarizer import summarize_text

# Load API Key & Custom Search Engine ID from .env
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    st.error("❌ API Key or CSE ID is missing. Please check the .env file.")

def google_search(query, num_results=5):
    """Fetches top Google search results using Custom Search API."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=num_results).execute()

        if "items" not in res:
            return []
        
        results = res["items"]
        return results

    except Exception as e:
        st.error(f"Google Search Error: {str(e)}")
        return []

def display_google_results(query):
    """Displays Google search results and summaries."""
    st.write(f"### Search Results for: {query}")

    results = google_search(query)

    if not results:
        st.warning("No results found.")
        return

    combined_text = ""
    
    for item in results:
        title = item.get("title", "No Title")
        link = item.get("link", "#")
        snippet = item.get("snippet", "No Description Available.")

        combined_text += snippet + " "  # Gather for summarization

        st.write(f"### [{title}]({link})")
        st.write(snippet)

    # Summarize search results
    summary = summarize_text(combined_text)
    st.write("### 🔥 Quick Summary of Search Results:")
    st.write(summary)
