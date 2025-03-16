import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

def debug_code(code):
    """Analyze Python code for errors and provide detailed debugging explanations."""
    prompt = f"""
    You are an expert Python developer and code reviewer.
    Your task is to analyze the following Python code and:
    - Identify syntax errors, logical mistakes, and inefficiencies.
    - Explain each detected issue in simple terms.
    - Provide the corrected version of the code.

    Code to analyze:
    ```python
    {code}
    ```

    Format your response as:
    **Detected Issues:**
    - Issue 1: [Explanation]
    - Issue 2: [Explanation]

    **Fixed Code:**
    ```python
    [Corrected Code]
    ```
    """

    response = client.chat.completions.create(
        model="gpt-4o",  # Use "gpt-3.5-turbo" if needed
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Example Usage
if __name__ == "__main__":
    buggy_code = """
def get_max_value(numbers):
    max = None
    for num in numbers
        if max is None or num > max:
            max = num
    return max
"""

    debug_result = debug_code(buggy_code)
    print("Debugging Report:\n", debug_result)
