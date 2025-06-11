---
title: Career_Assistant
app_file: app.py
sdk: gradio
sdk_version: 4.44.1
---

<p align="center">
  <img src="https://raw.githubusercontent.com/asherfeldman/Career_Assistant/main/.github/assets/banner.png" alt="Career Assistant Banner" />
</p>

<p align="center">
  <a href="https://huggingface.co/spaces/asherfeldman/Career_Assistant"><img alt="HuggingFace Spaces" src="https://img.shields.io/badge/Live%20Demo-HuggingFace-darkviolet?logo=huggingface&logoColor=white"></a>
  <a href="https://github.com/asherfeldman/Career_Assistant/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://www.python.org/downloads/"><img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue.svg"></a>
  <a href="https://github.com/asherfeldman/Career_Assistant/actions"><img alt="CI" src="https://github.com/asherfeldman/Career_Assistant/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/asherfeldman/Career_Assistant/commits/main"><img alt="Last Commit" src="https://img.shields.io/github/last-commit/asherfeldman/Career_Assistant?style=flat"></a>
  <a href="https://github.com/asherfeldman/Career_Assistant/issues"><img alt="Issues" src="https://img.shields.io/github/issues/asherfeldman/Career_Assistant?color=important"></a>
  <a href="https://github.com/asherfeldman/Career_Assistant/pulls"><img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/asherfeldman/Career_Assistant?color=success"></a>
</p>

<h1 align="center">Career Assistant 👩‍💼👨‍💼</h1>

Career Assistant is an interactive LLM-powered web app that answers questions about **Asher Feldman's** professional experience. Think of it as a conversational, always-on digital résumé: it converts Asher's LinkedIn profile and summary into a chat-friendly interface with built-in quality control to keep answers accurate, concise, and professional.

## ✨ Demo

👉 **Try it out now:** [https://huggingface.co/spaces/asherfeldman/Career_Assistant](https://huggingface.co/spaces/asherfeldman/Career_Assistant)

## 📜 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Features
- **Conversational Q&A** – Ask anything about Asher's background, skills, or projects.
- **Contextual Awareness** – Primed with a PDF export of the LinkedIn profile *and* a hand-curated summary.
- **Automated Quality Gate** – Every LLM response is reviewed by a second, lightweight model; sub-par answers are automatically rewritten.
- **Pig Latin Easter Egg** – Mention "patents" to see what happens. 🐷
- **Modern UI** – Built with Gradio 4 for a clean, responsive interface.

## 🛠 Tech Stack
- 🐍 Python 3.10+
- 🤗 [Gradio](https://gradio.app/) 4.44 for the web front-end
- 🦜🔗 OpenAI GPT-4o-mini for generation, O3-mini for evaluation
- 📄 pypdf for parsing the LinkedIn PDF
- 🔑 python-dotenv for environment management  

All dependencies are pinned in [`requirements.txt`](requirements.txt).

## ⚡️ Quick Start

1. **Clone & install**

   ```bash
   git clone https://github.com/asherfeldman/Career_Assistant.git
   cd Career_Assistant
   pip install -r requirements.txt
   ```

2. **Add your API keys**

   ```bash
   cp .env.example .env
   # then edit .env and set OPENAI_API_KEY=...
   ```

3. **Run locally**

   ```bash
   python app.py
   ```

4. Open your browser at the printed URL (defaults to `http://localhost:7860`) and start chatting!

> **Docker user?**  
> Simply run:  
> `docker compose up --build`

## 🧠 How It Works

```mermaid
flowchart TD
    A[User Question] --> B{Chat LLM (GPT-4o-mini)}
    B --> C[Draft Answer]
    C --> D{Evaluator LLM (O3-mini)}
    D -- Acceptable --> E[Show Answer]
    D -- Needs Fix --> F[Rewrite Prompt With Feedback]
    F --> B
```

1. A user sends a question.
2. The main LLM generates a draft answer using both the PDF and summary as system context.
3. The evaluator model scores the reply for accuracy, professionalism, and engagement.
4. If the score is low, feedback is injected and the response is regenerated; else it is returned.

## 📁 Project Structure

```
Career_Assistant/
├── app.py           # Main Gradio app & chat logic
├── evaluator.py     # Evaluation datamodel & helper functions
├── asher.pdf        # Full LinkedIn profile
├── asher_summary.txt# 14-line summary of experience
├── requirements.txt # Pinned dependencies
└── README.md
```

## 🗺 Roadmap
- [ ] Add vector-store retrieval for even deeper context.
- [ ] Multi-modal support (embed project screenshots & PDFs).
- [ ] CI/CD to auto-deploy to HuggingFace on push to `main`.

## 🤝 Contributing
Contributions are welcome! Please open an [issue](https://github.com/asherfeldman/Career_Assistant/issues) or start a [discussion](https://github.com/asherfeldman/Career_Assistant/discussions).

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/awesome‐feature`)
3. Commit your changes (`git commit -m 'feat: add awesome feature'`)
4. Push to the branch (`git push origin feat/awesome‐feature`)
5. Open a pull request

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) spec and run `pre-commit` before pushing.

## 🪪 License
Released under the [MIT License](LICENSE).

---

<p align="center">
Made with ❤️ and lots of coffee by <a href="https://www.linkedin.com/in/asherfeldman/">Asher Feldman</a>
</p>
