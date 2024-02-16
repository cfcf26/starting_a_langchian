from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import ( format_to_openai_tool_messages )
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

from langchain.agents import tool
from langchain.schema.agent import AgentFinish
from langchain.agents import AgentExecutor

from image_caption import load_image_caption
from youtube_loader import load_youtube
from web_loader import load_web_v2
from summarize_documents import summarize
from save_to_notion import save_to_notion

from langchain_openai import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

def summarize_to_notion(url, documents, type):
    summaries = summarize(llm, documents)
    save_to_notion(url, summaries, type)

@tool
def summarize_web(url):
    """Describes a web page"""
    documents = load_web_v2(url)
    summarize_to_notion(url, documents, 'Web')
    return AgentFinish(log="summarize_web", return_values={"output": "작업 완료!"})
    
@tool
def summarize_youtube(url):
    """Describes a youtube video"""
    documents = load_youtube(url)
    summarize_to_notion(url, documents, 'Youtube')
    return AgentFinish(log="summarize_youtube", return_values={"output": "작업 완료!"})
    
@tool
def summarize_image(url):
    """Describes an image"""
    documents = load_image_caption(url)
    summarize_to_notion(url, documents, 'Image')
    return AgentFinish(log="summarize_image", return_values={"output": "작업 완료!"})

tools = [summarize_web, summarize_youtube, summarize_image]

def URLAgent(llm, input):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You need to look at the URL and invoke the appropriate tool.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="URL_judgment"),
        ]
    )

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "URL_judgment": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    list(agent_executor.stream({"input": input}))