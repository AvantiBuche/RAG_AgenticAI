# RAG_AgenticAI

## [Vedic Astrology Expert Assistant using RAG, Ollama, Agno, LanceDB, and Streamlit](https://github.com/AvantiBuche/RAG_AgenticAI/blob/main/VedicAstrologyExpertAssistant.py)

### Overview
The goal was to create a chatbot capable of answering questions based on the classical Vedic astrology text - Brihat Jyotish Shastra.

The application allows users to ask astrology-related questions while the AI retrieves relevant information from the source document and uses it to generate context-aware responses.

### Execution Flow
User Question ↓ Streamlit ↓ Agent.run() ↓ Search LanceDB ↓ Retrieve PDF Chunks ↓ Add Context ↓ Llama 3.2 ↓ Generate Response ↓ Stream Response ↓ Display in UI

### Architecture
I have used 5 main components in this application.

Streamlit (Chat UI)

↓

Agno Agent

↓

Llama 3.2 (Ollama)

↓

RAG

↓

LanceDB (vector DB)

↓

Brihat Jyotish Shastra PDF (Document)

#### 1. Streamlit
It provides the chat interface where users can interact with the AI assistant in real time.

#### 2. Agno Agent Framework
Agno Agent acts as the orchestration layer. It manages conversation history, retrieves knowledge from the vector database, injects context into prompts, and communicates with LLM.

#### 3. Ollama + Llama 3.2 3B
I am running language model locally using Ollama. reasons: no API costs, offline inference, and full local control. I have used Llama 3.2 with 3B parameters.

#### 4. Embeddings
I have used mxbai-embed-large embedder to transform document chunks into numerical vectors. These embeddings allow the system to understand semantic meaning rather than relying only on keyword matching.

#### 5. LanceDB
LanceDB is used for vector storage, semantic search, hybrid retrieval, fast document lookup. Once the PDF content is converted into vector embeddings, it is stored inside LanceDB.

PDF -> Read -> Chunk -> Embed -> Store in LanceDB

### RAG Pipeline
PDF Document -> Chunking -> Embedding Generation -> Vector Storage (LanceDB) -> User Query -> Semantic Search -> Relevant Chunks Retrieved -> Context Added To Prompt -> LLM Response Generation

### Chunking Strategy
One important challenge I faced in RAG systems is handling large documents. To solve this, the PDF is split into manageable chunks using fixed-size chunking.

Chunk Size: 1000 characters
Overlap: 100 characters

The overlap helps preserve context between neighbouring chunks and improves retrieval quality.

### Memory and Conversation Context
This assistant also maintains conversation memory like historical context retention and improved follow-up question handling.

The agent remembers:

User: "My moon sign is Taurus"

User: "What impact will Saturn in 7th house have?"

The second question can use information from the first.

### Why Hybrid Search?

I have used hybrid search, combining - Keyword Search & Semantic Vector Search. It improves retrieval accuracy. This allows pure keyword or pure vector search in domain-specific applications.


