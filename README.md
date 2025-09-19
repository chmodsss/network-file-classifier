# PDF Networking Document Classifier

This project extracts text from PDF networking documents and classifies them based on the following categories:

1. Whether the document is technical (related to networking knowledge) or non-technical  
2. Main topics covered (e.g., wi-fi, routing, switching, 5g, edge computing)  
3. Networking vendor mentioned (e.g., Cisco, Juniper, Nokia)

Classification is done via OpenAI's GPT-4 model, integrated through LangChain, with structured JSON output validated by Pydantic.

---

## Features

- PDF text extraction using LangChain's `PyPDFLoader`
- Classification prompt enforces strict JSON output format
- Output parsed and validated by Pydantic models for robust typing
- Modular design for easy extensibility and integration with other tools
- Batch processing of multiple PDFs in a folder

---

## Setup

1. Clone the repository  
2. Install dependencies:

`pip install -r requirements.txt`

3. Set your OpenAI API key as an environment variable in `.env` file

---

## Usage

1. Place your PDF files in the `src/` directory or any folder you prefer  
2. Adjust `folder` and parameters in `main.py` if needed
3. Run the classification script:

`python main.py`

4. Classification results are printed to the console as JSON-like dictionaries per file

---

## File Structure

- `pdf_reader.py` — Loads and extracts text from PDFs using LangChain  
- `classifier.py` — Contains the OpenAI Chat LLM call with structured prompt and output parsing via Pydantic  
- `main.py` — Entry point: orchestrates batch processing of PDFs and prints results  
- `config.py` — (Optional) Stores prompt templates and configuration constants  
- `src/` — Folder where your PDF files reside  

---