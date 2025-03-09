import os
import json
import re
import spacy

# Load spaCy model for sentence segmentation
nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    """
    Clean the text by:
      - Replacing multiple whitespace characters (including line breaks) with a single space.
      - Removing common header/footer patterns (example: 'Page X of Y').
      - Stripping leading/trailing whitespace.
    """
    # Collapse all whitespace to a single space
    cleaned = re.sub(r'\s+', ' ', text)
    # Remove common header/footer pattern (example pattern, adjust as needed)
    cleaned = re.sub(r'Page \d+ of \d+', '', cleaned)
    return cleaned.strip()

def dynamic_chunk_text(text, target_token_count=300):
    """
    Dynamically split text into chunks based on sentence boundaries.
    
    This function uses spaCy to split the text into sentences, then groups sentences until
    reaching a target token count. This helps ensure that each chunk is coherent and aligned
    with natural language boundaries.
    
    Parameters:
      - text: The cleaned text.
      - target_token_count: The approximate number of words per chunk.
    
    Returns:
      - List of text chunks.
    """
    doc = nlp(text)
    chunks = []
    current_chunk = []
    current_count = 0
    for sent in doc.sents:
        sent_text = sent.text.strip()
        sent_tokens = sent_text.split()
        sent_token_count = len(sent_tokens)
        
        # If adding the sentence would exceed the target and we have a chunk, finalize it
        if current_chunk and (current_count + sent_token_count > target_token_count):
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent_text]
            current_count = sent_token_count
        else:
            current_chunk.append(sent_text)
            current_count += sent_token_count
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def process_extracted_text(input_file="extracted_text.json", output_file="processed_chunks.json", target_token_count=300):
    """
    Process extracted text from a JSON file by cleaning and dynamically chunking it.
    
    Each entry in the input JSON should be a dictionary with at least:
      - "pdf": the PDF file name,
      - "page": the page number,
      - "text": the extracted text from that page.
    
    For each entry, the function cleans the text and splits it into chunks based on sentence boundaries.
    Each chunk is stored along with metadata including which PDF, which page, and the chunk index.
    
    The processed data is saved as JSON to output_file.
    """
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found. Please run the PDF extraction step first.")
        return
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    processed_chunks = []
    for entry in data:
        pdf = entry.get("pdf", "unknown.pdf")
        page = entry.get("page", 0)
        text = entry.get("text", "")
        if not text:
            continue
        
        # Clean the text from the page
        cleaned_text = clean_text(text)
        # Dynamically chunk the cleaned text based on sentences
        chunks = dynamic_chunk_text(cleaned_text, target_token_count=target_token_count)
        
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "pdf": pdf,
                "page": page,
                "chunk_index": i + 1,  # 1-indexed
                "text": chunk
            })
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_chunks, f, indent=4, ensure_ascii=False)
    
    print(f"Processed text chunks saved to '{output_file}'.")

def main():
    # You can adjust target_token_count as needed (200-500 words is typical)
    process_extracted_text(target_token_count=300)

if __name__ == "__main__":
    main()
