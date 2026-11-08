# Main Streamlit application
import os
import json
import streamlit as st

from generator import generate_lesson
from evaluator import evaluate_lesson
from memory import load_memory, save_feedback


# Create output folder
os.makedirs("outputs", exist_ok=True)

st.set_page_config(
    page_title="RAG Lesson Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Self-Evaluating RAG Lesson Generator")

st.write(
    "An AI-powered system that generates, evaluates "
    "and improves beginner-friendly educational lessons."
)

st.subheader("Lesson Details")

st.info(
    "Topic: Introduction to Retrieval-Augmented Generation (RAG)"
)

st.write(
    "Target audience: Indian students who have completed "
    "12th grade and have limited English knowledge."
)

# Test option for the Loom demonstration
test_error = st.checkbox(
    "Inject a deliberate factual error for evaluator testing"
)

if st.button("Generate and Evaluate Lesson"):

    feedback = ""
    rejection_log = []
    approved_lesson = None

    # Initial generation + maximum two retries
    for attempt in range(3):

        st.subheader(f"Generation Attempt {attempt + 1}")

        with st.spinner("Generating lesson using Gemini AI..."):

            memory_context = load_memory()

            try:
                lesson = generate_lesson(
                    feedback=feedback,
                    memory_context=memory_context
                )

            except Exception as error:
                st.error(f"Generation failed: {error}")
                break

        # Inject the deliberate error only into the first attempt
        if test_error and attempt == 0:
            lesson += (
                "\n\nTesting statement: "
                "RAG updates the model weights."
            )

        st.write("Lesson generated successfully.")

        with st.spinner("Evaluating lesson quality..."):

            evaluation = evaluate_lesson(lesson)

        st.write("### Evaluation Results")

        st.json(evaluation)

        if evaluation["overall_status"] == "PASS":

            approved_lesson = lesson

            st.success(
                f"Lesson APPROVED on attempt {attempt + 1}!"
            )

            break

        else:

            st.error("Lesson REJECTED: Quality checks failed.")

            rejection_log.append({
                "attempt": attempt + 1,
                "status": "FAIL",
                "evaluation": evaluation
            })

            # Save feedback for future generations
            save_feedback(evaluation)

            feedback = json.dumps(
                evaluation,
                indent=4
            )

    # Save rejection log
    with open(
        "outputs/rejection_log.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            rejection_log,
            file,
            indent=4
        )

    # Display and save approved lesson
    if approved_lesson:

        with open(
            "outputs/final_lesson.md",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(approved_lesson)

        st.success("Final lesson saved successfully!")

        st.subheader("Approved Final Lesson")

        st.markdown(approved_lesson)

        st.download_button(
            label="Download Approved Lesson",
            data=approved_lesson,
            file_name="final_lesson.md",
            mime="text/markdown"
        )

    else:

        st.error(
            "The lesson did not pass after the initial attempt "
            "and two retries. No lesson was approved."
        )

    st.subheader("Rejection Log")

    st.json(rejection_log)

    st.success("Evaluation process completed.")
