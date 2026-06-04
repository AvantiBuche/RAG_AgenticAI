from agno.agent.agent import Agent
from agno.models.groq import Groq

import streamlit as st
from agno.agent import Agent
#from agno.embedder.ollama import OllamaEmbedder
from agno.models.ollama import Ollama
#from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
#from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType

from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()


dataloader = Agent(
    name="data loader",
    role="Reads CSV, Excel, or SQLite files into a DataFrame",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="You are a data loader who reads the data or file and loads or converts into dataframe",
    tools=[DuckDuckGoTools()],
    markdown=True,
)
#
cleaning = Agent(
    name="cleaning",
    role="Data cleaner",
    model=Groq(id="openai/gpt-oss-120b"),
    instructions="You are a data cleaner who removes duplicates, fills/drops nulls, fixes data types.",
    tools=[DuckDuckGoTools()],
    markdown=True,
)
analyst = Agent(
    name="Analyst",
    role="Data Analyst",
    model=Groq(id="openai/gpt-oss-120b"),
    instructions="You are a data analyst who analyzes data, computes descriptive stats, correlations, and detects trends, predictions, sales, profit, loss, everything which is included in data analysis",
    tools=[DuckDuckGoTools()],
    markdown=True,
)

visualize = Agent(
    name="Visualize",
    role="Data visualizer",
    model=Groq(id="openai/gpt-oss-120b"),
    instructions=" Generates bar, trend, graphs, pe chart and correlation charts and any of the possible charts which shows the analysis and as PNG files.",
    tools=[DuckDuckGoTools()],
    markdown=True,
)
report = Agent(
    name="Report",
    role="Report of Data Analysis",
    model=Groq(id="openai/gpt-oss-120b"),
    instructions="Generates an executive report in a story telling form",
    tools=[DuckDuckGoTools()],
    markdown=True,
)
analyst_team = Team(
    model=Groq(id="openai/gpt-oss-120b"),
    members=[dataloader, cleaning, analyst, visualize, report],
    name="analyst_team",
    instructions="""
    You are a analyst team that helps lead, analyze, visualize, and generate report team.
    First, load the data, read the data to gather information, analyze it, visualize it, and create report.
    """,
    show_members_responses=True,
    get_member_information_tool=True,
    #add_member_tools_to_context=True,
    #add_history_to_context=True,
)

analyst_team.print_response("Analysis report",stream=True)





