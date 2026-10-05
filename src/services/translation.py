import json
import os
import re

import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
REQUEST_TIMEOUT = 55


class TranslationError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def _parse_translation_response(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    raise TranslationError("Could not parse translation from model response", 502)


def translate_note(title: str, content: str, target_language: str) -> dict:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise TranslationError("Translation service is not configured", 503)

    model = os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)
    user_prompt = (
        f"Translate the following note title and content into {target_language}. "
        "Preserve meaning and tone. Return ONLY valid JSON with exactly these keys: "
        '"title" and "content". No markdown fences or extra text.\n\n'
        f"Title: {title}\n\nContent:\n{content}"
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional translator. Output only JSON.",
            },
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.environ.get("OPENROUTER_HTTP_REFERER", "https://mynotetaking.vercel.app"),
        "X-Title": "MyNoteTaking",
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise TranslationError(f"OpenRouter request failed: {exc}", 502) from exc

    if not response.ok:
        detail = response.text[:500] if response.text else response.reason
        raise TranslationError(f"OpenRouter error ({response.status_code}): {detail}", 502)

    data = response.json()
    try:
        message_content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise TranslationError("Unexpected OpenRouter response format", 502) from exc

    parsed = _parse_translation_response(message_content)
    if "title" not in parsed or "content" not in parsed:
        raise TranslationError("Translation response missing title or content", 502)

    return {
        "title": str(parsed["title"]),
        "content": str(parsed["content"]),
        "target_language": target_language,
        "model": model,
    }
