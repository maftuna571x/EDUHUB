import json
import requests

from django.conf import settings


def generate_quiz_question(
    level="B1",
    topic="General English",
):
    """
    Generate one English multiple-choice quiz question
    using Cloudflare Workers AI.
    """

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/"
        f"@cf/meta/llama-3.1-8b-instruct"
    )

    prompt = f"""
You are an expert English language teacher creating
high-quality English learning quizzes.

Create ONE multiple-choice English question.

CEFR level: {level}
Topic: {topic}

Requirements:

1. The question must genuinely test English.
2. Use natural, grammatically correct English.
3. Create exactly four answer options.
4. Only ONE answer must be correct.
5. The incorrect answers must be plausible.
6. Give a short and useful explanation.
7. Match the requested CEFR level.
8. Do not use Uzbek.
9. Return ONLY valid JSON.
10. Do not use Markdown.
11. Do not add any text before or after the JSON.

Return exactly this structure:

{{
    "question": "Your question here",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct_answer": "A",
    "explanation": "Short explanation",
    "level": "{level}",
    "topic": "{topic}",
    "difficulty": "MEDIUM"
}}
"""

    response = requests.post(
        url,
        headers={
            "Authorization": (
                f"Bearer {settings.CLOUDFLARE_API_TOKEN}"
            ),
            "Content-Type": "application/json",
        },
        json={
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional English teacher "
                        "and quiz creator."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise RuntimeError(
            f"Cloudflare AI returned an error: {data}"
        )

    result = data.get("result")

    if result is None:
        raise RuntimeError(
            f"Cloudflare AI returned no result: {data}"
        )

    # ---------------------------------------------------------
    # Cloudflare can return the generated content in
    # different formats depending on the model.
    # ---------------------------------------------------------

    text = None

    if isinstance(result, dict):

        # Most common response format
        if "response" in result:
            text = result["response"]

        # Alternative format
        elif "text" in result:
            text = result["text"]

        # Sometimes the result itself is already JSON
        else:
            text = result

    else:
        text = result

    # ---------------------------------------------------------
    # If Cloudflare already returned a Python dictionary,
    # return it directly.
    # ---------------------------------------------------------

    if isinstance(text, dict):
        return normalize_quiz_question(text)

    # ---------------------------------------------------------
    # Convert response to string
    # ---------------------------------------------------------

    text = str(text).strip()

    # ---------------------------------------------------------
    # Remove Markdown code fences if the AI accidentally
    # returns ```json ... ```
    # ---------------------------------------------------------

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "")
        text = text.strip()

    # ---------------------------------------------------------
    # Convert JSON string to Python dictionary
    # ---------------------------------------------------------

    try:
        question = json.loads(text)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Cloudflare AI did not return valid JSON.\n\n"
            f"Raw response:\n{text}"
        ) from exc

    return normalize_quiz_question(question)


def normalize_quiz_question(question):
    """
    Validate and normalize the generated quiz question.
    """

    if not isinstance(question, dict):
        raise RuntimeError(
            "Generated quiz question is not a JSON object."
        )

    required_fields = [
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
        "explanation",
        "level",
        "topic",
        "difficulty",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in question
    ]

    if missing_fields:
        raise RuntimeError(
            "Cloudflare AI returned an incomplete question. "
            f"Missing fields: {', '.join(missing_fields)}"
        )

    # Normalize correct answer
    question["correct_answer"] = (
        str(question["correct_answer"])
        .strip()
        .upper()
    )

    if question["correct_answer"] not in {
        "A",
        "B",
        "C",
        "D",
    }:
        raise RuntimeError(
            "Invalid correct_answer returned by AI: "
            f"{question['correct_answer']}"
        )

    # Normalize level
    question["level"] = (
        str(question["level"])
        .strip()
        .upper()
    )

    allowed_levels = {
        "A1",
        "A2",
        "B1",
        "B2",
        "C1",
        "C2",
    }

    if question["level"] not in allowed_levels:
        raise RuntimeError(
            f"Invalid CEFR level returned by AI: "
            f"{question['level']}"
        )

    # Normalize difficulty
    question["difficulty"] = (
        str(question["difficulty"])
        .strip()
        .upper()
    )

    allowed_difficulties = {
        "EASY",
        "MEDIUM",
        "HARD",
    }

    if question["difficulty"] not in allowed_difficulties:
        question["difficulty"] = "MEDIUM"

    # Convert important values to strings
    for field in [
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "explanation",
        "topic",
    ]:
        question[field] = str(question[field]).strip()

    return question
