#agent with rag and streamlit

import streamlit as st
from agno.agent import Agent
from agno.document.chunking.fixed import FixedSizeChunking
from agno.embedder.ollama import OllamaEmbedder
from agno.models.ollama import Ollama
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType

@st.cache_resource
def get_knowledge_base():
    embedder = OllamaEmbedder(id="mxbai-embed-large", dimensions=1024)
    vector_db = LanceDb(
        table_name="jyotish_Shastra",
        uri="/tmp/lancedb",
        search_type=SearchType.hybrid,
        embedder=embedder
    )
    knowledge_base = PDFKnowledgeBase(
        path="Brihat_Jyotish_Shastra.pdf",
        vector_db=vector_db,
        chunking_strategy = FixedSizeChunking(
        overlap=100,
        chunk_size=1000
    ),
    )

    # Load the knowledge base on the first run
    knowledge_base.load(upsert=True)
    return knowledge_base

def stream_response(agent, prompt):
    response = agent.run(prompt, stream=True)
    for chunk in response:
        if chunk.content is None:
            continue
        if "search_knowledge_base(" in chunk.content:
            continue
        yield chunk.content

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    st.session_state.agent = Agent(
        model=Ollama(id="llama3.2:3b", options={"num_ctx": 16192}),
        knowledge=get_knowledge_base(),
        add_context=True,
        add_references=True,
        description="You are an expert in Vedic astrology and Jyotish who gives predictions",
        instructions=[
            "Use additional data provided analysis and predictions for charts",
            "Analyze the charts, dashas, transits, timings, houses, planets for the user to give prediction"
        ],
        search_knowledge=True,
        add_history_to_messages=True,
        num_history_responses=10,
        show_tool_calls=True,
        markdown=True,
        debug_mode=False,
    )

agent = st.session_state.agent


st.title("Chat with the Vedic Astrologer expert")
prompt = st.chat_input("Your question")
if prompt:
    st.session_state.messages.append({'role': 'user', 'text': prompt})
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['text'])
    with st.chat_message('assistant'):
        response = st.write_stream(stream_response(agent, prompt))
        st.session_state.messages.append({'role': 'assistant', 'text': response})




