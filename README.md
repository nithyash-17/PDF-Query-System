# PDF Ingestion & Query App with Hugging Face

This project implements a full-stack application for ingesting PDF files, processing their content, and providing a question-answering interface. The backend is built with Node.js and Express, which orchestrates a series of Python scripts to:

- **Extract text** from PDF files using PyPDF2.
- **Preprocess and chunk** the extracted text using spaCy and custom logic.
- **Generate embeddings** using a local Hugging Face model (via SentenceTransformers) and build a FAISS index.
- **Process queries** by converting the user query into an embedding, retrieving the most relevant text chunks, building a prompt, and generating an answer using a local LLM (e.g., EleutherAI/gpt-j-6B).

> **Note:**  
> The Hugging Face API key (if needed) is stored in an environment file (e.g., `.env`) and is excluded from the repository via `.gitignore`.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **PDF Ingestion:** Upload multiple PDF files via a web interface.
- **Text Extraction:** Extract text from each page using Python (PyPDF2).
- **Preprocessing & Chunking:** Clean and split extracted text into manageable chunks.
- **Embedding Generation & FAISS Indexing:** Generate embeddings using a Hugging Face model and build a FAISS index for similarity search.
- **Query Processing & Answer Generation:** Convert a query into an embedding, retrieve relevant text chunks, build a prompt, and generate an answer using a local LLM.
- **Integrated Frontend & Backend:** A Node.js server handles the entire pipeline and serves a Bootstrap-based frontend.


## Requirements

### Python Dependencies

- **Python 3.7+**
- [PyPDF2](https://pypi.org/project/PyPDF2/) – For extracting text from PDFs.
- [spaCy](https://spacy.io/) – For advanced text preprocessing and sentence segmentation.
  - Download the English model:  
    ```bash
    python -m spacy download en_core_web_sm
    ```
- [sentence-transformers](https://www.sbert.net/) – For generating text embeddings using Hugging Face models.
- [faiss-cpu](https://github.com/facebookresearch/faiss) – For building the FAISS index.
- [numpy](https://numpy.org/) – For numerical operations.
- [transformers](https://github.com/huggingface/transformers) – For local text-generation models.
- [torch](https://pytorch.org/) – Required backend for Hugging Face models.

Install all required Python packages with:

```bash
pip install PyPDF2 spacy sentence-transformers faiss-cpu numpy transformers torch
python -m spacy download en_core_web_sm
Node.js Dependencies
Express
Multer – For handling file uploads.
python-shell or you can use Node’s child_process (this repository uses python-shell by default).
cors – For handling Cross-Origin Resource Sharing.
Install Node.js dependencies in the project root with:

bash
Copy
Edit
npm install express multer python-shell cors
Installation & Setup
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Install Node.js Dependencies:

bash
Copy
Edit
npm install
Set Up the Python Environment:

Ensure Python 3.7 or higher is installed.
Install the required Python packages as described above.
Make sure the folder structure is correct:
Create a folder named pdfs in the project root.
Place all your Python scripts in the python-scripts folder.
Place your frontend files (e.g., index.html) in the public folder.
Configure Environment Variables:

Create a .env file in the project root for sensitive configuration (e.g., your Hugging Face API key):
ini
Copy
Edit
HUGGINGFACE_API_KEY=your_actual_api_key_here
The .env file is included in .gitignore so it won’t be pushed to GitHub.
Running the Application
Start the Node.js Server:

In the project root, run:

bash
Copy
Edit
node server.js
You should see a console message like:

arduino
Copy
Edit
Server running at http://localhost:3000
Access the Frontend:

Open your web browser and navigate to http://localhost:3000. Use the provided forms to:

Upload PDFs:
Upload your PDF files using the Upload form. The backend will run the ingestion pipeline by executing:

pdf_to_text.py (extracts text),
preprocess_text.py (cleans and chunks text),
create_embeddings.py (generates embeddings and builds a FAISS index).
Submit a Query:
After ingestion, use the Query form to enter a question. The backend will process your query by running query_engine.py, which retrieves relevant text chunks, builds a prompt, and generates a final answer using a local Hugging Face text-generation model. The final answer and related data will be displayed on the frontend.

Troubleshooting
"Cannot GET /":
Ensure there is an index.html file in the public folder.

Python Script Errors:
Run individual Python scripts (e.g., python python-scripts/pdf_to_text.py) manually to verify they work correctly.

File Path Issues:
If your Python scripts cannot locate the pdfs folder, adjust the file paths in your scripts to use absolute paths based on the project structure.

Environment Variables:
Ensure your .env file is set up correctly and that your Python scripts read from it if needed.

CORS & Fetch Issues:
If your frontend fails to fetch data from the backend, confirm that you’re accessing your site via http://localhost:3000 and that the backend server is running.







[Watch Demo](https://github.com/nithyash-17/PDF-Query-System/blob/main/demo.mp4)
