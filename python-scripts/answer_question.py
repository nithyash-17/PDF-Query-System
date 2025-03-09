import sys
import json
from transformers import pipeline

def get_answer(prompt):
    """
    Generate an answer using a local Hugging Face text generation model.
    Here we use EleutherAI/gpt-j-6B as an example.
    Adjust max_length and temperature as needed.
    """
    # If you have a GPU, you can set device=0; otherwise, omit device to use CPU.
    generator = pipeline("text-generation", model="EleutherAI/gpt-j-6B", device=0)  
    result = generator(prompt, max_length=len(prompt.split()) + 150, temperature=0.2, num_return_sequences=1)
    # Remove the prompt from the generated text to obtain just the answer
    generated_text = result[0]["generated_text"]
    answer = generated_text[len(prompt):].strip()
    return answer

def main():
    # Check if prompt is provided as a command-line argument
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No prompt provided"}))
        return
    
    # The prompt is expected to be passed as the first command-line argument.
    prompt = sys.argv[1]
    answer = get_answer(prompt)
    
    # Output the answer as a JSON string.
    print(json.dumps({"answer": answer}))

if __name__ == "__main__":
    main()
