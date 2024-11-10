import os
from typing import Tuple

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str, mock=False) -> Tuple[Summary, str]:
    load_dotenv()

    if mock == False:
        linkedin_username = linkedin_lookup_agent(name=name)
    else:
        linkedin_username = 'mockuser'

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=mock)

    summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    # llm = ChatOllama(temperature=0, model=os.environ.get("OLLAMA_MODEL"))
    llm = ChatOpenAI(temperature=0, model_name=os.environ.get("OPENAI_MODEL"))

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Jeroen de Bruijn", mock=True)
