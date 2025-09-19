import os
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

    def __init__(self, mock_flag=True, model="gpt-4o-mini"):
        self.mock_flag = mock_flag
        self.model = model

    def classify_text_with_llm(self, text: str) -> ClassificationResult:
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
        text = load_pdf_text(filepath)
        if self.mock_flag:
            classification = self.classify_text_mock(text)
        else:
            classification = self.classify_text_with_llm(text)
        return {"filepath": filepath, **classification.model_dump()}

    def classify_pdfs(self, folder_path: str):
        pdf_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith(".pdf")
        ]
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.process_single_pdf, pdf_files))
        return results
