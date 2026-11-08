# Lesson generation logic
import os
from dotenv import load_dotenv
from google import genai

from prompts import LESSON_GENERATION_PROMPT, REPAIR_INSTRUCTIONS

# Load the API key from the .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Check whether the API key exists
if not API_KEY:
    raise ValueError(
        "Gemini API key not found. Please check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def generate_lesson(feedback="", memory_context=""):
    """
    Generate a beginner-friendly RAG lesson.

    feedback: Evaluator feedback from the previous attempt.
    memory_context: Lessons learned from previous runs.
    """

    prompt = LESSON_GENERATION_PROMPT

    if feedback:
        prompt += "\n\nPREVIOUS EVALUATOR FEEDBACK:\n"
        prompt += feedback
        prompt += "\n\n" + REPAIR_INSTRUCTIONS

    if memory_context:
        prompt += "\n\nIMPORTANT LEARNINGS FROM PREVIOUS RUNS:\n"
        prompt += memory_context

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()

    except Exception as error:
        print("Error while generating lesson:", error)
        raise
