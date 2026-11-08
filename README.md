# Self-Evaluating GenAI Lesson Generator

# Self-Evaluating RAG Lesson Generator

## Project Overview

This project is an AI-powered educational content generation system that creates, evaluates, and improves beginner-friendly lessons on Retrieval-Augmented Generation (RAG).

The system uses Gemini AI to generate educational content and evaluate it against a quality rubric.

## Problem Statement

AI-generated educational content may contain factual errors, unexplained technical terms, or confusing explanations.

This project addresses these problems through automated evaluation, rejection, feedback, and regeneration.

## Key Features

- AI-powered lesson generation.
- Automated PASS/FAIL quality evaluation.
- Six evaluation criteria.
- Automatic rejection of lessons that fail evaluation.
- Regeneration with evaluator feedback.
- Persistent memory for previous failures.
- Deliberate factual error detection.
- Approved lesson download in Markdown format.
- Rejection log generation.

## Technology Stack

- Python
- Google Gemini API
- Streamlit
- JSON
- Python-dotenv

## Evaluation Criteria

1. Accuracy
2. Beginner Friendliness
3. Examples
4. Jargon Explanation
5. Key Topic Coverage
6. Flow and Structure

A lesson is approved only when all six evaluation criteria pass.

## Workflow

1. Generate a lesson using Gemini AI.
2. Evaluate the generated lesson.
3. Check the six quality criteria.
4. Reject the lesson if any criterion fails.
5. Save evaluator feedback in persistent memory.
6. Regenerate the lesson with improvement instructions.
7. Approve the lesson only after it passes evaluation.
8. Save the final lesson and rejection log.

The system supports one initial generation and a maximum of two retries.

## Project Structure

```text
NxtWave_GenAI_Assignment/
│
├── app.py
├── generator.py
├── evaluator.py
├── memory.py
├── prompts.py
├── requirements.txt
├── .env
├── .gitignore
│
├── memory/
│   └── feedback_memory.json
│
└── outputs/
    ├── final_lesson.md
    └── rejection_log.json
```

## Installation

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## API Configuration

Create a `.env` file in the project folder.

Add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Never upload your API key to GitHub.

## Run the Application

Execute:

```bash
python -m streamlit run app.py
```

Open the local Streamlit URL displayed in your terminal.

## Testing

The application includes an option to inject a deliberate factual error.

For testing:

1. Enable the deliberate error checkbox.
2. Generate the lesson.
3. Observe the evaluator detecting the incorrect claim.
4. Observe the rejection and feedback.
5. Observe regeneration and final approval.

## Output

The application generates:

- `final_lesson.md` – approved educational lesson.
- `rejection_log.json` – record of rejected attempts.

## Conclusion

This project demonstrates an AI-assisted educational content pipeline with automated quality evaluation, feedback-driven regeneration, and persistent memory.