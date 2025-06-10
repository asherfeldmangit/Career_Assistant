"""
evaluator.py - Evaluation context and prompt setup for Career_Assistant

This module loads context from PDF and summary files, and prepares the system prompt for the evaluator LLM that checks the quality of agent responses.
"""
from pydantic import BaseModel
from pypdf import PdfReader


reader = PdfReader("context/asher.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("context/asher_summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

class Evaluation(BaseModel):
    """
    Data model for evaluation results.

    Attributes:
        is_acceptable (bool): Whether the agent's response is acceptable.
        feedback (str): Feedback or reason for rejection.
    """
    is_acceptable: bool
    feedback: str

evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of a digital assistant on a person's website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on the person in the form of their summary and LinkedIn details. Here's the information:"

evaluator_system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."

