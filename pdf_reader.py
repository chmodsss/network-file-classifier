from langchain_community.document_loaders import PyPDFLoader


def load_pdf_text(pdf_path: str) -> str:
    """
    Load PDF text from the given path using Langchain's PyPDFLoader.
    Returns concatenated text from all pages.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    full_text = "\n".join(doc.page_content for doc in documents)
    return full_text
