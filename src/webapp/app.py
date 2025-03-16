import re
import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

def clean_ai_output(text):
    """Remove unnecessary Markdown formatting and return issues separately from fixed code."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove **bold markers**
    text = re.sub(r"^- ", "", text, flags=re.MULTILINE)  # Remove list markers '- '
    text = text.strip()

    # Extract the "Fixed Code" separately
    fixed_code_match = re.search(r"Fixed Code:\s*```python(.*?)```", text, re.DOTALL)
    if fixed_code_match:
        fixed_code = fixed_code_match.group(1).strip()
        text = re.sub(r"Fixed Code:\s*```python.*?```", "", text, flags=re.DOTALL).strip()  # Remove fixed code from explanation
    else:
        fixed_code = "No fixed code generated."

    return text, fixed_code  # Returns (issues explanation, fixed code)

def ai_debug_code(code):
    """Send code to GPT-4o for debugging, optimization, and fixing."""
    prompt = f"""
    Analyze the following Python code for:
    - Syntax errors and logical mistakes.
    - Computational inefficiencies (e.g., O(n²) to O(n)).
    - Memory optimizations.
    - Code readability and best practices.

    If you detect an inefficient algorithm, return an optimized version with:
    - A step-by-step explanation of why the new approach is better.
    - A revised version of the code that improves time complexity.

    Code to analyze:
    ```python
    {code}
    ```

    Format the response as:
    Detected Issues:
    Issue 1: [Explanation]
    Issue 2: [Explanation]

    Fixed Code:
    ```python
    [Optimized & Corrected Code]
    ```
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response.choices[0].message.content
    explanation, fixed_code = clean_ai_output(ai_output)  # Apply text cleaning

    return explanation, fixed_code  # Return both explanations and fixed code separately


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_code = request.form["code"]
        debug_result, fixed_code_result = ai_debug_code(user_code)
    else:
        user_code = ""  # Clears textarea on refresh
        debug_result = None  # Clears detected issues on refresh
        fixed_code_result = None  # Clears fixed code output on refresh

    return render_template("index.html", user_code=user_code, debug_result=debug_result, fixed_code_result=fixed_code_result)


if __name__ == "__main__":
    app.run(debug=True)
