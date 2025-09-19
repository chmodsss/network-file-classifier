import os
import time
import threading
import logging
import concurrent.futures
from pdf_reader import load_pdf_text
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional
from config import CLASSIFIER_PROMPT
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]


class ClassificationResult(BaseModel):
    is_technical: bool
    topics: List[str]
    vendor: Optional[str]


output_parser = PydanticOutputParser(pydantic_object=ClassificationResult)


class Classifier:

    def __init__(self, mock_flag=False, model="gpt-4o", max_calls_per_minute=60):
        """
        Initialize the Classifier.

        Args:
            mock_flag (bool): If True, use mock classification instead of LLM.
            model (str): The OpenAI LLM model name to use.
            max_calls_per_minute (int): Maximum allowed LLM calls per minute.
        """
        self.mock_flag = mock_flag
        self.model = model
        self.max_calls_per_minute = max_calls_per_minute
        self.call_interval = 60.0 / max_calls_per_minute
        self._lock = None
        self._last_call_time = 0

    def _ensure_lock(self):
        """
        Ensure that a threading lock is initialized for throttling.
        """
        if self._lock is None:
            self._lock = threading.Lock()

    def _throttle(self):
        """
        Throttle calls to the LLM to avoid exceeding the rate limit.
        """
        self._ensure_lock()
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            wait_time = self.call_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            self._last_call_time = time.time()

    def classify_text_with_llm(self, text: str) -> ClassificationResult:
        """
        Classify the given text using the LLM and return the classification result.

        Args:
            text (str): The text to classify.

        Returns:
            ClassificationResult: The result of the classification.
        """
        self._throttle()
        logger.info("LLM classification invoked.")

        classification_prompt = CLASSIFIER_PROMPT.format(text=text)
        prompt = (
            output_parser.get_format_instructions() + "\n\n" + classification_prompt
        )

        llm = ChatOpenAI(model_name=self.model, temperature=0)
        response = llm.invoke([HumanMessage(content=prompt)])

        classification = output_parser.parse(response.content)

        return classification

    def classify_text_mock(self, text: str) -> ClassificationResult:
        """
        Return a mock classification result for testing purposes.

        Args:
            text (str): The text to classify.

        Returns:
            ClassificationResult: The mock classification result.
        """
        self._throttle()
        logger.info("Mock classification invoked.")
        sample_output = """```json
        {
        "is_technical": true,
        "topics": ["wi-fi", "routing", "switching", "5g"],
        "vendor": "Cisco"
        }```
        """

        classification = output_parser.parse(sample_output)

        return classification

    def process_single_pdf(self, filepath: str):
        """
        Process and classify a single PDF file using either the LLM or a mock function, based on mock_flag.

        Args:
            filepath (str): Path to the PDF file.

        Returns:
            dict: A dictionary containing the file path and classification result.
        """
        try:
            text = load_pdf_text(filepath)
            if self.mock_flag:
                classification = self.classify_text_mock(text)
            else:
                classification = self.classify_text_with_llm(text)
            return {"filepath": filepath, **classification.model_dump()}
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}", exc_info=True)
            return {"filepath": filepath, "error": str(e)}

    def classify_pdfs(self, folder_path: str):
        """
        Classify all PDF files in a folder in parallel using multiple processes.

        Args:
            folder_path (str): Path to the folder containing PDF files.

        Returns:
            list: A list of classification results for each PDF file.
        """
        pdf_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith(".pdf")
        ]
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.process_single_pdf, pdf_files))
        return results
