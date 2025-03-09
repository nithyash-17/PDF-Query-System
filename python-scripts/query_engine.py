import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import os
from dotenv import load_dotenv

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Hide TF logs
tf.get_logger().setLevel('ERROR')         # Hide TF warnings


load_dotenv()

# Retrieve API Key
AI_API_KEY = os.getenv("AI_API_KEY")


# 🔹 Replace with your Hugging Face API key
HUGGINGFACE_API_KEY = AI_API_KEY

# 🔹 Use a valid Hugging Face model for inference
HF_MODEL_NAME = "tiiuae/falcon-7b-instruct"  # Change if needed

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}", "Content-Type": "application/json"}

def get_embedding(text, model):
    """Generate an embedding for the given text using the SentenceTransformer model."""
    return model.encode(text)

def query_index(query, index, metadata, model, top_k=3):
    """Retrieve the top-k similar text chunks from the FAISS index."""
    query_embedding = get_embedding(query, model)
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    # Search in FAISS index
    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []
    for idx in indices[0]:
        if idx != -1:
            retrieved_chunks.append(metadata[idx])

    return retrieved_chunks

def create_prompt(query, retrieved_chunks):
    """Create a detailed prompt using retrieved chunks."""
    context = "\n".join([f"- {chunk['text']}" for chunk in retrieved_chunks])

    prompt = f"""
    You are an AI assistant. Answer the following question based only on the given context.

    Context:
    {context}

    Question: {query}

    Answer:
    """.strip()

    return prompt

"""def get_answer(prompt):
    Generate an answer using Hugging Face API.
    payload = {
        "inputs": prompt,  # Only send the text, without embeddings
        "parameters": {"max_new_tokens": 300, "temperature": 0.2}
    }
    
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()[0].get("generated_text", "No answer generated.").strip()
    else:
        return f"Error: {response.json()}"
"""
def get_answer(prompt):
    """Generate an answer using Hugging Face API and extract only the relevant response."""
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.2}
    }
    
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        full_response = response.json()[0].get("generated_text", "").strip()
        
        # Extract only the final answer by splitting at "Answer:" and taking the last part
        answer = full_response.split("Answer:")[-1].strip()
        return answer if answer else "No answer generated."
    else:
        return f"Error: {response.json()}"

def main():
    print("Started script execution.")
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided."}))
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"Query received: {query}")

    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load FAISS index
    index = faiss.read_index("faiss_index.index")

    # Load metadata
    with open("metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Retrieve similar chunks
    retrieved_chunks = query_index(query, index, metadata, model, top_k=3)

    if not retrieved_chunks:
        print(json.dumps({"error": "No relevant context found."}))
        sys.exit(1)

    # Create LLM prompt
    prompt = create_prompt(query, retrieved_chunks)
    
    print("\nGenerated Prompt:\n", prompt)  # Debugging

    # Generate answer from Hugging Face API
    answer = get_answer(prompt)

    # Output result
    output = {
        "answer": answer,
    }
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
