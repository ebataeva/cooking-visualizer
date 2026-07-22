"""Разбор рецепта через DeepSeek API (OpenAI-совместимый)."""

import json
import os
from pathlib import Path

import streamlit as st
from openai import OpenAI

from app.schema import validate_analysis

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system.md"

LANG_NAMES = {"ru": "Russian (русский)", "en": "English", "es": "Spanish (español)"}


class AnalyzerError(Exception):
    """Ошибка вызова API ("api:...") или невалидный JSON после retry ("invalid_json:...")."""


def get_api_key() -> str | None:
    """Ключ DeepSeek: st.secrets → env → ~/.deepseek_key → ввод в сайдбаре."""
    try:
        if "DEEPSEEK_API_KEY" in st.secrets:
            return st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        pass  # secrets.toml может отсутствовать локально
    if os.environ.get("DEEPSEEK_API_KEY"):
        return os.environ["DEEPSEEK_API_KEY"]
    key_file = Path.home() / ".deepseek_key"
    if key_file.exists():
        key = key_file.read_text(encoding="utf-8").strip()
        if key:
            return key
    return st.session_state.get("user_api_key") or None


@st.cache_data(show_spinner=False)
def analyze(recipe_text: str, lang: str, _api_key: str) -> dict:
    """Разобрать рецепт на языке lang. Кэш — по паре (текст, язык)."""
    client = OpenAI(api_key=_api_key, base_url=DEEPSEEK_BASE_URL)
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    lang_directive = (
        f"Answer language: {LANG_NAMES[lang]}. "
        f'The "lang" field of the JSON must be "{lang}". '
        "All content strings must be in this language. Units are always metric (г/g, мл/ml, °C)."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": lang_directive},
        {"role": "user", "content": recipe_text},
    ]

    data, errors = _call(client, messages)
    if errors:
        # один retry: возвращаем модели её ответ и список ошибок валидации
        messages.append({
            "role": "assistant",
            "content": json.dumps(data, ensure_ascii=False) if data else "(invalid JSON)",
        })
        messages.append({
            "role": "user",
            "content": (
                "Your JSON failed schema validation. Return the FULL corrected JSON "
                "only, no commentary. Errors:\n" + "\n".join(errors[:20])
            ),
        })
        data, errors = _call(client, messages)
    if errors:
        raise AnalyzerError("invalid_json:" + "; ".join(errors[:10]))
    return data


def _call(client: OpenAI, messages: list[dict]) -> tuple[dict | None, list[str]]:
    """Один вызов модели → (данные, ошибки валидации)."""
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=8000,
        )
    except Exception as e:
        raise AnalyzerError(f"api:{e}") from e
    try:
        data = json.loads(resp.choices[0].message.content)
    except (json.JSONDecodeError, TypeError) as e:
        return None, [f"JSON parse error: {e}"]
    return data, validate_analysis(data)
