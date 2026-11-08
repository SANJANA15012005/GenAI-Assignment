import json
import os

MEMORY_FOLDER = "memory"
MEMORY_FILE = os.path.join(MEMORY_FOLDER, "feedback_memory.json")


def load_memory():
    os.makedirs(MEMORY_FOLDER, exist_ok=True)

    if not os.path.exists(MEMORY_FILE):
        return ""

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            lessons = data
        elif isinstance(data, dict):
            lessons = data.get("lessons_learned", [])
        else:
            lessons = []

        return "\n".join(str(item) for item in lessons)

    except (json.JSONDecodeError, OSError):
        return ""


def save_feedback(evaluation):
    os.makedirs(MEMORY_FOLDER, exist_ok=True)

    data = {"lessons_learned": []}

    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

            if isinstance(existing_data, dict):
                data = existing_data
            elif isinstance(existing_data, list):
                data["lessons_learned"] = existing_data

        except (json.JSONDecodeError, OSError):
            pass

    suggestions = evaluation.get("improvement_suggestions", [])
    failed_checks = []

    for name, details in evaluation.items():
        if isinstance(details, dict):
            if details.get("status") == "FAIL":
                failed_checks.append(
                    f"{name}: {details.get('reason', '')}"
                )

    feedback = failed_checks + suggestions

    lessons = data.get("lessons_learned", [])
    lessons.extend(str(item) for item in feedback)

    data["lessons_learned"] = lessons[-20:]

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data