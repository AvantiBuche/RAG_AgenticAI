from agno.agent.agent import Agent
from agno.models.groq import Groq

from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools import DuckDuckGoSearchRun


researcher = Agent(
    name="researcher",
    role="Research Assistant",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="You are a research assistant. Find information and provide detailed analysis.",
    tools=[DuckDuckGoSearchRun()],
    markdown=True,
)
#
writer = Agent(
    name="writer",
    role="Content Writer",
    model=Groq(id="openai/gpt-oss-120b"),
    instructions="You are a content writer. Create well-structured content based on research.",
    tools=[DuckDuckGoTools()],
    markdown=True,
)

research_team = Team(
    model=Groq(id="openai/gpt-oss-120b"),
    members=[researcher, writer],
    name="research_team",
    instructions="""
    You are a research team that helps users with research and content creation.
    First, use the researcher to gather information, then use the writer to create content.
    """,
    show_members_responses=True,
    get_member_information_tool=True,
    #add_member_tools_to_context=True,
    #add_history_to_context=True,
)

research_team.print_response("future of AI in India",stream=True)
