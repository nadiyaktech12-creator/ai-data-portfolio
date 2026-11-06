import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_groq import ChatGroq
from langchain_core.documents import Document

load_dotenv()

# Page config
st.set_page_config(
    page_title="Enterprise Document QA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        background-color: #1e2130;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    h1 {
        color: #4f9dff;
    }
    .stExpander {
        background-color: #161b22;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Enterprise Document QA")
st.caption("Hybrid RAG • Dense + BM25 Retrieval")

@st.cache_resource
def load_system():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    data = vectorstore.get()
    texts = data.get("documents", [])
    metadatas = data.get("metadatas", [])

    lc_docs = [Document(page_content=t, metadata=m or {}) for t, m in zip(texts, metadatas)]
    bm25_retriever = BM25Retriever.from_documents(lc_docs)
    bm25_retriever.k = 6

    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.1)
    return dense_retriever, bm25_retriever, llm

def hybrid_retrieve(dense_retriever, bm25_retriever, query, k=5):
    dense_docs = dense_retriever.invoke(query)
    bm25_docs = bm25_retriever.invoke(query)
    seen = set()
    combined = []
    for doc in dense_docs + bm25_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            combined.append(doc)
    return combined[:k]

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info("Documents loaded from `data/` folder")
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Load system
with st.spinner("Loading Hybrid RAG system..."):
    dense_retriever, bm25_retriever, llm = load_system()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            docs = hybrid_retrieve(dense_retriever, bm25_retriever, prompt)
            context = "\n\n".join([d.page_content for d in docs])
            full_prompt = f"""Use the following context to answer the question clearly and accurately.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {prompt}

Answer:"""
            answer = llm.invoke(full_prompt).content

            st.markdown(answer)

            # Sources
            with st.expander("📚 View Sources"):
                for i, doc in enumerate(docs, 1):
                    source = doc.metadata.get("source", "unknown")
                    page = doc.metadata.get("page", "")
                    st.markdown(f"**{i}.** `{Path(source).name}`" + (f" — page {page}" if page != "" else ""))

    st.session_state.messages.append({"role": "assistant", "content": answer})