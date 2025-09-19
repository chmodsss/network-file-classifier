# PDF Networking Document Classifier

This project extracts text from PDF networking documents and classifies them based on the following categories:

1. Whether the document is technical (related to networking knowledge) or non-technical  
2. Main topics covered (e.g., wi-fi, routing, switching, 5g, edge computing)  
3. Networking vendor mentioned (e.g., Cisco, Juniper, Nokia)

Classification is done via OpenAI's GPT-4 model, integrated through LangChain, with structured JSON output validated by Pydantic.

---

## Features

- PDF text extraction using LangChain’s `PyPDFLoader`

- Strict classification prompt enforcing `JSON` output format for consistent, machine-readable results.

- Parsing and validation of classification output with Pydantic models, ensuring robust data typing.

- Parallel processing of multiple PDFs using Python’s `concurrent.futures` to speed up batch classification.

- API rate limit enforcement via throttling, controlling LLM calls to avoid exceeding usage quotas and unexpected costs.

- Flexible execution modes:
  - As a standalone Python application for batch processing from command line.
  - As a FastAPI REST API endpoint for integration with other services.
  - As a Streamlit interactive UI web app for easy user interaction.

- Mock classification functionality, enabling offline testing without actual LLM API calls.

- Comprehensive logging for monitoring, debugging, and traceability.


---

## Setup

1. Clone the repository
   ```
   git clone https://github.com/chmodsss/network-file-classifier
   ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Add your OpenAI API key as an environment variable in `.env` file
   ```
   OPENAI_API_KEY="sk-proj-lK78q....."
   ```

---

## Usage

1. Place your PDF files in the `pdf_files/` directory or any folder you prefer  

2. Adjust `INPUT_DIR`, `OUTPUT_DIR` and `TEMP_DIR` in `config.py` file if needed

3. Run the application:
   1. Execute `python main.py` from command line to run the applicaion in console mode
   2. Execute `uvicorn app:app --reload` to access the application via api endpoints at `localhost:8000/docs`
   3. Execute `streamlit run streamlitapp.py` to run the application via a web UI at `localhost:8501`

4. Classification results are written to the `OUTPUT_DIR` as well as printed to the console


---

## NOTE:
* Before running the application, make sure the `mock_flag` is set to `False` in `main.py` or `app.py` or `streamlitapp.py`, whichever one you wishes to run. Setting it to False ensures that the application runs LLM calls to classify the pdfs. For testing purposes and not to waste any api credits, set the flag to True
* If needed, change the name of the OpenAI chat model in `main.py` or `app.py` or `streamlitapp.py` before running the application.

---

## File Structure

- `main.py` — Entry point: orchestrates batch processing of PDFs and prints results
- `streamlitapp.py` - Runs the application in a web UI
- `app.py` - Publishes the application via API endpoints
- `pdf_reader.py` — Loads and extracts text from PDFs using LangChain  
- `classifier.py` — Contains the OpenAI Chat LLM call with structured prompt and output parsing via Pydantic
- `config.py` — Stores prompt templates and configuration constants  
- `writer.py` - Handles saving classification results to a timestamped JSON file.
- `pdf_files/` — Folder where your PDF files reside
- `output/` - Folder where the output files are stored
- `.temp_uploads/` - Folder will be managed by streamlit and FastAPI to store uploaded files
---