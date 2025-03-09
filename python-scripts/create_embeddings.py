import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def main():
    # Load processed text chunks from the JSON file produced by preprocess_text.py
    with open("processed_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    embeddings = []
    metadata = []
    
    # Load a local Hugging Face embedding model (e.g., all-MiniLM-L6-v2)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Process each chunk: generate an embedding and store metadata
    for chunk in chunks:
        print(f"Embedding chunk {chunk['chunk_index']} from {chunk['pdf']} (page {chunk['page']})...")
        # Generate embedding for the chunk text
        embedding = model.encode(chunk["text"])
        embeddings.append(embedding)
        metadata.append(chunk)
    
    # Convert the list of embeddings into a numpy array (FAISS requires float32)
    embedding_dim = len(embeddings[0])
    embedding_array = np.array(embeddings).astype("float32")
    
    # Create a FAISS index using L2 (Euclidean) distance
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embedding_array)
    
    # Save the FAISS index to a file for later retrieval
    faiss.write_index(index, "faiss_index.index")
    # Save the metadata (chunk information) to a JSON file
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    print("Embeddings created and stored. FAISS index and metadata saved.")

if __name__ == "__main__":
    main()
