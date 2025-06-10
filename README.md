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

- `context/asher.pdf`: The full LinkedIn profile of Asher Feldman, used to provide detailed background information.
- `context/asher_summary.txt`: A concise summary of Asher Feldman's professional experience.

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
2. Ensure you have the required context files in the `context/` directory.
3. Run the assistant:
   ```
   python Assisstant/main.py
   ```
4. Interact with the assistant via the Gradio web interface.
