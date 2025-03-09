import os
import json
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from each page of a PDF file.
    Returns a list of dictionaries, where each dictionary contains:
      - 'pdf': PDF file name,
      - 'page': Page number,
      - 'text': Extracted text from that page.
    """
    extracted = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    extracted.append({
                        "pdf": os.path.basename(pdf_path),
                        "page": page_num + 1,
                        "text": text.strip()
                    })
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return extracted

def main():
    # Folder where PDF files are stored
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up (project root) and then join with 'pdfs'
    pdf_folder = os.path.join(os.path.dirname(current_dir), 'pdfs')
    # Output JSON file where extracted text will be stored
    output_file = "extracted_text.json"
    
    all_extracted = []
    print("pdf_to_text.py started")
    
    if not os.path.exists(pdf_folder):
        print(f"Folder '{pdf_folder}' does not exist. Please create it and add your PDF files.")
        return
    
    # Iterate over all PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {pdf_path}...")
            extracted = extract_text_from_pdf(pdf_path)
            all_extracted.extend(extracted)
    
    # Save the extracted text to a JSON file
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(all_extracted, out_file, indent=4, ensure_ascii=False)
    
    print(f"Extraction complete. Extracted text saved to '{output_file}'.")

if __name__ == "__main__":
    main()
