"""
main.py - Interactive digital representative for Asher Feldman

This module loads context from PDF and summary files, sets up system prompts, and provides a Gradio web interface for users to interact with an LLM-based agent. The agent answers questions about Asher Feldman's career, with automatic evaluation and retry logic for quality control.
"""
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from pydantic import BaseModel
import gradio as gr
import json

load_dotenv(override=True)
openai = OpenAI()

reader = PdfReader("context/asher.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("context/asher_summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Asher Feldman"

system_prompt = f"You are acting as {name}'s digital representative. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, invent something perposterous but highly complimentary and make it sound like you know what you're talking about. \
If that happens, try to veer the conversation back to answering career related questions."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}'s digital representative."

css = """
/* Make chat font larger and stylized */
.gr-chat-message, .gr-chat-message-text, .gr-chatbot, .gr-chatbot-message, .gr-chatbot-message-text {
    font-size: 1.35rem !important;
    font-family: 'Fira Mono', 'JetBrains Mono', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', monospace !important;
    letter-spacing: 0.02em;
    line-height: 1.7;
    color: #2d2d2d;
    background: #f7f7fa;
    border-radius: 8px;
    padding: 8px 16px;
}
"""


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of a digital assistant on a person's website. \
The Agent shouldn't lie, but it's okay to be vague if you don't know the answer. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on the person in the form of their summary and LinkedIn details. Here's the information:"

evaluator_system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."

def evaluator_user_prompt(reply, message, history):
    """
    Constructs the user prompt for the evaluator model, summarizing the conversation and the latest exchange.

    Args:
        reply (str): The agent's latest reply.
        message (str): The user's latest message.
        history (list): The conversation history as a list of dicts.

    Returns:
        str: The formatted prompt for the evaluator model.
    """
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += f"Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

def evaluate(reply, message, history) -> Evaluation:
    """
    Evaluates the agent's reply using the evaluator LLM.

    Args:
        reply (str): The agent's reply to evaluate.
        message (str): The user's message.
        history (list): The conversation history.

    Returns:
        Evaluation: The evaluation result, including acceptability and feedback.
    """
    messages = [
        {"role": "system", "content": evaluator_system_prompt},
        {"role": "user", "content": evaluator_user_prompt(reply, message, history) + "\n\nReply in the following JSON format: {\"is_acceptable\": true/false, \"feedback\": \"...\"}"}
    ]
    response = openai.chat.completions.create(
        model="o3-mini",
        messages=messages
    )
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return Evaluation(**data)
    except Exception as e:
        return Evaluation(is_acceptable=False, feedback=f"Failed to parse model output: {content}\nError: {e}")

messages = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": "do you hold a patent?"}]
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
reply = response.choices[0].message.content


def rerun(reply, message, history, feedback):
    """
    Retries generating a reply if the previous one was rejected by the evaluator, incorporating feedback and context.

    This function updates the system prompt to include the previous (rejected) answer and the evaluator's feedback, then re-asks the LLM to generate a new reply. This helps the agent learn from its mistakes and produce a higher-quality response.

    Args:
        reply (str): The previous agent reply that was rejected.
        message (str): The user's message.
        history (list): The conversation history.
        feedback (str): Feedback from the evaluator explaining why the previous reply was rejected.

    Returns:
        str: The new agent reply, generated with the additional context and feedback.
    """
    updated_system_prompt = system_prompt + f"\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

def chat(message, history):
    """
    Handles a chat interaction: generates a reply, evaluates it, and retries if necessary.

    Args:
        message (str): The user's message.
        history (list): The conversation history.

    Returns:
        str: The agent's final reply (after passing evaluation).
    """
    if "patent" in message:
        system = system_prompt + "\n\nEverything in your reply needs to be in pig latin - \
              it is mandatory that you respond only and entirely in pig latin"
    else:
        system = system_prompt
    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply =response.choices[0].message.content

    evaluation = evaluate(reply, message, history)
    
    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print("Failed evaluation - retrying")
        print(evaluation.feedback)
        reply = rerun(reply, message, history, evaluation.feedback)       
    return reply

# --- Gradio Interface ---
"""
Launches the Gradio web interface for the Career Assistant.

This interface allows users to interact with the digital representative in a chat format. The chat function handles message processing, evaluation, and retries, ensuring only high-quality responses are shown to the user. The interface uses custom CSS for improved readability and style.

- To use: Run this script and follow the link to the Gradio web UI in your browser.
- The chat history is preserved for each session.
- The interface is launched with sharing enabled and opens in the browser automatically.
"""
gr.ChatInterface(chat, type="messages", css=css).launch(share=True, inbrowser=True)

