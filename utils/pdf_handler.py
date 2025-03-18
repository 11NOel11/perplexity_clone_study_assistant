import fitz  # PyMuPDF for PDF text extraction

def extract_text_from_pdf(pdf_file):
    """Extracts text from a given PDF file."""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc if page.get_text("text"))
        return text.strip() if text else "No readable text found in PDF."
    except Exception as e:
        return f"Error extracting text: {e}"