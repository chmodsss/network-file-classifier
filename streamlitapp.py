import streamlit as st
import os
from config import TEMP_DIR
from concurrent.futures import ThreadPoolExecutor
from classifier import Classifier

c = Classifier(mock_flag=False, model="gpt-4o")

st.title("Network File Classification App")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files", type="pdf", accept_multiple_files=True
)


def classify_file(file_path):
    return c.process_single_pdf(file_path)


if uploaded_files:
    os.makedirs(TEMP_DIR, exist_ok=True)

    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)

        # Save uploaded file temporarily
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_paths.append(file_path)

    # Process files in parallel (adjust max_workers as needed)
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(classify_file, file_paths))

    # Clean up temp files
    for file_path in file_paths:
        os.remove(file_path)

    st.subheader("Classification Results")
    for res in results:
        st.json(res)
