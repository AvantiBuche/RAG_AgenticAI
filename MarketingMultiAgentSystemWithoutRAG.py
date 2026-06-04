#multi-agent with rag and streamlit

import streamlit as st
from agno.agent import Agent
#from agno.knowledge.chunking.fixed import FixedSizeChunking for 2.5.14
from agno.document.chunking.fixed import FixedSizeChunking
#from agno.knowledge.embedder.ollama import OllamaEmbedder for 2.5.14
from agno.embedder.ollama import OllamaEmbedder
from agno.models.ollama import Ollama
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
#from agno.knowledge.reader.pdf_reader import PDFReader for 2.5.14
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def create_agents():

    research_agent = Agent(
        model=Ollama(id="llama3.1:8b"),
        description="Marketing research expert",
        instructions=[
        "Use the knowledge base internally.",
        "Never show tool calls.",
        "Pass only a plain text query to tools.",
        "Never show JSON schemas.",
        "Only return the final answer."],
        tools=[DuckDuckGoTools()()],
        markdown=True,
    )
    audience_agent = Agent(
        model=Ollama(id="llama3.2:3b"),
        description="Target audience expert"
    )
    content_agent = Agent(
        model=Ollama(id="llama3.2:3b"),
        description="Marketing copywriter",
        tools=[DuckDuckGoSearchRun()],
        markdown=True,
    )
    seo_agent = Agent(
        model=Ollama(id="llama3.2:3b"),
        description="SEO specialist"
    )
    social_agent = Agent(
        model=Ollama(id="llama3.2:3b"),
        description="Social media strategist"
    )
    image_agent = Agent(
        model=Ollama(id="llama3.2:3b"),
        description="Image prompt engineer"
    )
    return {
        "research": research_agent,
        "audience": audience_agent,
        "content": content_agent,
        "seo": seo_agent,
        "social": social_agent,
        "image": image_agent
    }

@st.cache_resource
def get_marketing_agents():
    return create_agents()

def marketing_manager(query):

    agents = get_marketing_agents()

    research = agents["research"].run(
        f"Research this marketing request: {query}"
    )
    audience = agents["audience"].run(
        f"Identify target audience for: {query}"
    )
    content = agents["content"].run(
        f"Create marketing copy for: {query}"
    )
    seo = agents["seo"].run(
        f"Generate SEO keywords for: {query}"
    )
    social = agents["social"].run(
        f"Create Instagram, LinkedIn and X content for: {query}"
    )
    image = agents["image"].run(
        f"Create image generation prompt for: {query}"
    )
    return f"""
# Market Research
{research.content}
# Target Audience
{audience.content}
# Marketing Copy
{content.content}
# SEO Keywords
{seo.content}
# Social Media Posts
{social.content}
# Image Prompt
{image.content} """

if "messages" not in st.session_state:
    st.session_state.messages = []
if 'marketing_ready' not in st.session_state:
    st.session_state.marketing_ready = True
# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])


st.title("Chat with AI Marketing Agency")
prompt = st.chat_input("Your question")
if prompt:
    st.session_state.messages.append({'role': 'user', 'text': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
        response = marketing_manager(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({
        "role": "assistant",
        "text": response
        })



