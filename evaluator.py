# Lesson evaluation logic
import os
import json
import re

from dotenv import load_dotenv
from google import genai

from prompts import LESSON_EVALUATION_PROMPT

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env file.")

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def evaluate_lesson(lesson):
    """
    Evaluate the generated lesson.
    Return PASS or FAIL with detailed feedback.
    """

    prompt = LESSON_EVALUATION_PROMPT.replace(
        "{lesson}", lesson
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Evaluator returned an empty response.")

        result_text = response.text.strip()

        # Remove Markdown code fences if Gemini adds them
        result_text = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            result_text
        ).strip()

        result = json.loads(result_text)

        required_checks = [
            "accuracy",
            "beginner_friendliness",
            "examples",
            "jargon_explanation",
            "key_topic_coverage",
            "flow_and_structure"
        ]

        # Check that all six evaluation results exist
        for check in required_checks:
            if check not in result:
                raise ValueError(
                    f"Missing evaluation result: {check}"
                )

            status = result[check].get("status", "").upper()

            if status not in ["PASS", "FAIL"]:
                raise ValueError(
                    f"Invalid status for {check}"
                )

            result[check]["status"] = status

        # Hard rule: RAG does not directly retrain
        # or update the language model's weights.
        incorrect_claims = [
            "rag updates the model weights",
            "rag changes the model weights",
            "rag retrains the model",
            "rag trains the language model",
            "rag modifies the model weights"
        ]

        lesson_lower = lesson.lower()

        for claim in incorrect_claims:
            if claim in lesson_lower:
                result["accuracy"]["status"] = "FAIL"
                result["accuracy"]["reason"] = (
                    "Incorrect technical claim detected: "
                    + claim
                    + ". RAG retrieves external information "
                    "without directly retraining the model."
                )

        # Overall PASS only when every check passes
        all_passed = all(
            result[check]["status"] == "PASS"
            for check in required_checks
        )

        result["overall_status"] = (
            "PASS" if all_passed else "FAIL"
        )

        return result

    except Exception as error:
        print("Evaluation error:", error)

        return {
            "accuracy": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "beginner_friendliness": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "examples": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "jargon_explanation": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "key_topic_coverage": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "flow_and_structure": {
                "status": "FAIL",
                "reason": "Evaluation could not be completed."
            },
            "overall_status": "FAIL",
            "improvement_suggestions": [
                "Check the API connection and try again."
            ]
        }
