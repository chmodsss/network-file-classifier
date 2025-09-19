import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional
from config import CLASSIFIER_PROMPT
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]


class ClassificationResult(BaseModel):
    is_technical: bool
    topics: List[str]
    vendor: Optional[str]


output_parser = PydanticOutputParser(pydantic_object=ClassificationResult)


def classify_text_with_llm(
    text: str, model: str = "gpt-4o"
) -> ClassificationResult:
    classification_prompt = CLASSIFIER_PROMPT.format(text=text)
    prompt = (
        output_parser.get_format_instructions()
        + "\n\n"
        + classification_prompt
    )

    llm = ChatOpenAI(model_name=model, temperature=0)
    response = llm.invoke([HumanMessage(content=prompt)])

    classification = output_parser.parse(response.content)

    return classification
