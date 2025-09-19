import os
from langchain.chat_models import ChatOpenAI
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


# Create output parser from Pydantic model
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

    # Initialize OpenAI Chat LLM
    llm = ChatOpenAI(model_name=model, temperature=0)

    # Call the LLM with prompt wrapped in HumanMessage
    response = llm([HumanMessage(content=prompt)])

    # Parse the response content with the structured output parser
    classification = output_parser.parse(response.content)

    return classification
