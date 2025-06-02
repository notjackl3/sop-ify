import fitz  # pip install PyMuPDF

doc = fitz.open("converted.pdf")
for page_num, page in enumerate(doc):
    text_instances = page.search_for("YOUR_TARGET_TEXT")
    for inst in text_instances:
        print(f"Found on page {page_num + 1} at {inst}")
