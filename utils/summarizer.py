from transformers import T5ForConditionalGeneration, T5Tokenizer
import streamlit as st

@st.cache_resource
def load_summarizer():
    """Loads the T5-small model and tokenizer."""
    model_name = "t5-small"
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_summarizer()

def summarize_text(text, max_length=300, min_length=100):
    """Summarizes input text using T5."""
    if not text.strip():
        return "Error: The input text is empty."
    
    if len(text.split()) < 5:
        return "Error: The input text is too short to summarize."

    try:
        input_text = f"summarize: {text}"
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(
            input_ids, 
            max_length=max_length, 
            min_length=min_length, 
            length_penalty=2.0, 
            num_beams=4
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        return f"Summarization error: {str(e)}"
