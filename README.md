---
title: Career_Assistant
app_file: app.py
sdk: gradio
sdk_version: 4.44.1
---
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Last Commit](https://img.shields.io/github/last-commit/asherfeldman/Career_Assistant?style=flat)](https://github.com/asherfeldman/Career_Assistant/commits/main)

# Career_Assistant

Career_Assistant is an interactive web-based agent designed to answer questions about Asher Feldman's professional history, skills, and experience. It leverages large language models (LLMs) to provide engaging, professional, and contextually accurate responses, acting as a digital representative for Asher Feldman.

## Features

- **Conversational Agent:** Answers questions about Asher Feldman's career, background, and skills, using information extracted from a LinkedIn profile PDF and a curated summary.
- **Contextual Awareness:** The assistant is primed with both a detailed summary and the full LinkedIn profile text to ensure responses are relevant and accurate.
- **Quality Control:** Each response is automatically evaluated for quality and professionalism by a separate evaluator model before being returned to the user. If a response is deemed unacceptable, the agent will automatically retry with feedback.
- **Fun Easter Egg:** If a user asks about patents, the assistant will reply entirely in Pig Latin.

## Models Used

- **Main Conversational Model:** Uses OpenAI's `gpt-4o-mini` model to generate responses to user questions, ensuring high-quality, context-aware answers.
- **Evaluation Model:** Uses OpenAI's `o3-mini` model to critically assess the quality of each response, providing structured feedback and enforcing a high standard of professionalism and engagement.

## Data Sources

- `asher.pdf`: The full LinkedIn profile of Asher Feldman, used to provide detailed background information.
- `asher_summary.txt`: A concise summary of Asher Feldman's professional experience.

## Tech Stack

- **Python** with the following libraries:
  - `openai` for LLM access
  - `pypdf` for PDF parsing
  - `gradio` for the web interface
  - `python-dotenv` for environment variable management

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Ensure `asher.pdf` and `asher_summary.txt` are located in the project root (same directory as `app.py`).
3. Run the assistant:
   ```
   python app.py
   ```
4. Interact with the assistant via the Gradio web interface.

## Documentation

### Module Structure

- **app.py**: Main entry point. Loads context, sets up system prompts, defines the chat logic, evaluation, and retry mechanism, and launches the Gradio interface.
- **evaluator.py**: Contains the evaluation context and the `Evaluation` data model used for quality control.

### Main Classes and Functions

- **Evaluation (class)**: Pydantic model representing the result of a response evaluation (`is_acceptable`, `feedback`).
- **evaluator_user_prompt(reply, message, history)**: Formats the conversation and latest exchange for the evaluator model.
- **evaluate(reply, message, history)**: Uses the evaluator LLM to check if a response is acceptable.
- **rerun(reply, message, history, feedback)**: Retries generating a response if the previous one was rejected, incorporating feedback.
- **chat(message, history)**: Main chat handler. Generates a reply, evaluates it, and retries if necessary.

### Gradio Interface Example

When you run the project, a Gradio web interface will launch in your browser. You can interact with the assistant by sending messages. The assistant will:

- Generate a response using the main LLM.
- Evaluate the response for quality.
- Retry if the response is not acceptable.
- Return the final, approved response to you.

---

For further details, see the docstrings in the source code.
