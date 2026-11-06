
# Enterprise Document QA (Hybrid RAG)

https://enterprise-document-question-and-answers-hybrid-rag.streamlit.app/

A production-style **Hybrid Retrieval-Augmented Generation** system that answers questions over enterprise documents using both dense (vector) and sparse (BM25) retrieval.

Built with LangChain, Chroma, BM25, and Groq.

## Features

- Hybrid retrieval (Dense + BM25)
- PDF ingestion with chunking
- Persistent vector store (Chroma)
- Streamlit chat interface
- Source citations
- Local & free to run (Groq free tier)

## Project Structure

14_enterprise-document-qa/ ├── data/ # Place your PDFs here ├── src/ │ └── ingest.py # Ingest PDFs into Chroma ├── chroma_db/ # Vector store (auto-created) ├── app.py # Streamlit UI ├── requirements.txt ├── .env.example └── README.md
## Setup

1. **Clone the repo** and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
	2	Install dependencies: pip install -r requirements.txt
	3	
	4	Add your Groq API key:
	◦	Copy .env.example to .env
	◦	Add your key: GROQ_API_KEY=your_key_here
	◦	
	5	Add PDFs:
	◦	Put your documents inside the data/ folder.
	6	Ingest documents: python src/ingest.py
	7	
	8	Run the app: streamlit run app.py
	9	
Example Questions
	•	What is the vacation policy?
	•	What are the working hours?
	•	How do I reset the device?
	•	What is covered in the employee handbook?
Tech Stack
	•	LangChain + LangChain-Chroma
	•	Chroma (vector store)
	•	BM25 (sparse retrieval)
	•	Sentence-Transformers (embeddings)
	•	Groq (LLM)
	•	Streamlit (UI)
	•	PyPDF (document loading)
Notes
	•	This is a portfolio project demonstrating Hybrid RAG.
	•	All processing is local except the LLM call to Groq.
	•	Add more PDFs anytime and re-run src/ingest.py.




