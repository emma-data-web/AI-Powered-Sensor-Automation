import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-2.5-flash")


def build_summary_prompt(readings):
    return f"""
You are an industrial IoT monitoring assistant.

Below are recent sensor readings with predicted humidity errors.
Analyze them as a group (not row by row).

Tasks:
- Identify overall trends in the errors
- Detect abnormal or risky behavior
- Decide if operator action is needed
- Give clear, simple advice

Recent readings:
{readings}

Return a short summary in plain language.
"""


def summarize_recent_errors(readings):
    prompt = build_summary_prompt(readings)
    response = model.generate_content(prompt)
    return response.text
