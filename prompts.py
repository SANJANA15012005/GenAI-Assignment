# Prompts used by the generator and evaluator
LESSON_GENERATION_PROMPT = """
You are an expert educational content creator.

Your task is to create a complete beginner-friendly lesson on:

TOPIC: Introduction to Retrieval-Augmented Generation (RAG)

TARGET AUDIENCE:
An Indian student who has completed 12th grade.
The student has limited English and no advanced technical knowledge.

LESSON REQUIREMENTS:

1. Start with a simple introduction to RAG.
2. Explain why RAG is needed.
3. Explain how RAG works step by step.
4. Explain the important components:
   - Large Language Models (LLMs)
   - Documents and data
   - Embeddings
   - Vector databases
   - Retrieval
   - Augmented generation
5. Explain every technical word in simple English.
6. Include simple real-life examples.
7. Include one practical example of a RAG application.
8. Explain the difference between normal AI responses and RAG-based responses.
9. Include a short summary at the end.

IMPORTANT RULES:

- Use simple English.
- Avoid unnecessary technical jargon.
- Explain difficult terms immediately.
- Do not make false technical claims.
- Do not say that RAG directly changes or retrains a model's weights.
- Make the lesson easy to understand without needing another resource.
- Use clear headings and logical order.

Generate the complete lesson.
"""


LESSON_EVALUATION_PROMPT = """
You are a strict educational quality evaluator.

Evaluate the lesson provided below.

TOPIC: Introduction to Retrieval-Augmented Generation (RAG)

TARGET AUDIENCE:
An Indian student who has completed 12th grade
and has limited English.

Evaluate these six criteria:

1. ACCURACY:
Are the technical explanations correct?
Are there any false or misleading claims?

2. BEGINNER FRIENDLINESS:
Can a student with basic knowledge understand it?

3. EXAMPLES:
Does the lesson contain simple real-life examples?

4. JARGON EXPLANATION:
Are technical words explained in simple English?

5. KEY TOPIC COVERAGE:
Does it explain LLMs, documents, embeddings,
vector databases, retrieval and augmented generation?

6. FLOW AND STRUCTURE:
Does the lesson follow a clear and logical order?

STRICT EVALUATION RULES:

- Give PASS or FAIL for every criterion.
- If even one criterion fails, the overall result must be FAIL.
- Do not give PASS just to be encouraging.
- Identify factual errors clearly.
- Suggest specific improvements.

Return ONLY valid JSON in this format:

{
    "accuracy": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "beginner_friendliness": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "examples": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "jargon_explanation": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "key_topic_coverage": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "flow_and_structure": {
        "status": "PASS",
        "reason": "Explanation"
    },
    "overall_status": "PASS",
    "improvement_suggestions": []
}

LESSON TO EVALUATE:

{lesson}
"""


REPAIR_INSTRUCTIONS = """
The previous lesson failed the quality evaluation.

Read the evaluator's feedback carefully.

Regenerate the complete lesson and correct every identified problem.

Do not repeat the same mistakes.
Follow all the original lesson requirements.
Return only the corrected lesson.
"""
