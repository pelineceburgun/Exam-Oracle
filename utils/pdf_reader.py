from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file, max_chars=3000):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

        if len(text) >= max_chars:
            break

    return text[:max_chars]
