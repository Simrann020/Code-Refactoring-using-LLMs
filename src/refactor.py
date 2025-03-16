import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

def refactor_code(code):
    """Send code to GPT-4 and receive an optimized version."""
    prompt = f"Refactor the following Python code for better readability and performance:\n\n```python\n{code}\n```"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Example Usage
if __name__ == "__main__":
    sample_code = """
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j] and lst[i] not in duplicates:
                duplicates.append(lst[i])
    return duplicates


"""
    refactored = refactor_code(sample_code)
    print("Refactored Code:\n", refactored)
