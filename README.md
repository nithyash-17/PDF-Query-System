# PDF Ingestion & Query App with Hugging Face

This project implements a full-stack application for ingesting PDF files, processing their content, and providing a question-answering interface. The backend is built with Node.js and Express, which orchestrates a series of Python scripts to:

- **Extract text** from PDF files using PyPDF2.
- **Preprocess and chunk** the extracted text using spaCy and custom logic.
- **Generate embeddings** using a local Hugging Face model (via SentenceTransformers) and build a FAISS index.
- **Process queries** by converting the user query into an embedding, retrieving the most relevant text chunks, building a prompt, and generating an answer using a local LLM (e.g., EleutherAI/gpt-j-6B).

> **Note:**  
> The Hugging Face API key (if needed) is stored in an environment file (e.g., `.env`) and is excluded from the repository via `.gitignore`.



## Features

- **PDF Ingestion:** Upload multiple PDF files via a web interface.
- **Text Extraction:** Extract text from each page using Python (PyPDF2).
- **Preprocessing & Chunking:** Clean and split extracted text into manageable chunks.
- **Embedding Generation & FAISS Indexing:** Generate embeddings using a Hugging Face model and build a FAISS index for similarity search.
- **Query Processing & Answer Generation:** Convert a query into an embedding, retrieve relevant text chunks, build a prompt, and generate an answer using a local LLM.
- **Integrated Frontend & Backend:** A Node.js server handles the entire pipeline and serves a Bootstrap-based frontend.






[Watch Demo](https://github.com/nithyash-17/PDF-Query-System/blob/main/demo.mp4)
