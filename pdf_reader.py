from langchain_community.document_loaders import PyPDFLoader


def load_pdf_text(pdf_path: str) -> str:
    """
    Load and return the full text content of a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Concatenated text from all pages of the PDF.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    full_text = "\n".join(doc.page_content for doc in documents)
    return full_text
