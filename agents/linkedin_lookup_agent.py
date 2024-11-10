import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama  # TOOL STREAMING NOT SUPPORTED YET
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name=os.environ.get("OPENAI_MODEL"),
    )

    template = """given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_url = result["output"]

    return linkedin_url


if __name__ == "__main__":
    linkedin_url = lookup("Jeroen de Bruijn, Bright Alley, Netherlands")
    print(linkedin_url)
