"""Контракт структуры разбора рецепта.

Единый формат JSON, который: (1) генерирует DeepSeek по системному промпту,
(2) хранится в демо-файлах data/falafel_*.json, (3) потребляет render.py.
Все текстовые поля — на языке из поля "lang"; коды (necessity, accuracy) —
канонические, локализуются только при рендере через i18n.py.
"""

from jsonschema import Draft202012Validator

# Канонические коды — не переводятся в данных
NECESSITY = ["base", "important", "optional", "conditional"]
ACCURACY = ["verified", "estimated", "empirical"]  # ✓ / ~ / ?
COLUMNS = ["0", "½×", "¾×", "1×", "⁵⁄₄×", "3/2×"]  # фиксированный порядок матрицы
LANGS = ["ru", "en", "es"]

_variant = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "detail": {"type": "string"},
    },
    "required": ["title", "detail"],
    "additionalProperties": False,
}

_matrix_cell = {
    "type": "object",
    "properties": {
        # короткий вердикт (2–4 слова) — виден в свёрнутой матрице
        "verdict": {"type": "string"},
        # конкретное сенсорное/физическое последствие, 1–2 предложения
        "consequence": {"type": "string"},
        # ячейка входит в зону толерантности вокруг 1× (для визуальных «мостиков»)
        "in_zone": {"type": "boolean"},
        # значение определяется эмпирически (тест шарика и т.п.) → метка ?
        "empirical": {"type": "boolean"},
    },
    "required": ["verdict", "consequence", "in_zone"],
    "additionalProperties": False,
}

_ingredient = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "amount": {"type": "string"},  # метрические единицы: г, мл, ч.л.
        "necessity": {"enum": NECESSITY},
        # для conditional — обязательное объяснение, какую ошибку техники компенсирует
        "necessity_note": {"type": "string"},
        "matrix": {"type": "array", "items": _matrix_cell, "minItems": 6, "maxItems": 6},
        "variants": {"type": "array", "items": _variant},        # формы того же ингредиента
        "substitutions": {"type": "array", "items": _variant},   # замены другим ингредиентом
    },
    "required": ["name", "amount", "necessity", "matrix", "variants", "substitutions"],
    "additionalProperties": False,
}

_equipment = {
    "type": "object",
    "properties": {
        "device": {"type": "string"},   # «Ninja MAX PRO», «вручную» и т.п.
        "settings": {"type": "string"}, # «Air Fry 200°C, 12–14 мин» / «6–8 импульсов»
        "accuracy": {"enum": ACCURACY + [None]},  # метка точности настроек
    },
    "required": ["device", "settings"],
    "additionalProperties": False,
}

_step = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},      # глагол + краткое имя действия
        "what": {"type": "string"},       # максимум 2 предложения, без размытых формулировок
        "duration": {"type": "string"},   # «12–24 ч», «~12–14 мин» или условие
        "accuracy": {"enum": ACCURACY},   # уровень точности duration/температуры
        "equipment": _equipment,
        "done_when": {"type": "string"},  # сенсорный критерий готовности, не время
        "if_skipped": {"type": "string"}, # одно конкретное последствие
        # инструкция калибровки первой партии — обязательна для estimated-шагов аэрогриля
        "calibration": {"type": ["string", "null"]},
    },
    "required": ["title", "what", "duration", "accuracy", "equipment", "done_when", "if_skipped"],
    "additionalProperties": False,
}

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "lang": {"enum": LANGS},
        "dish": {"type": "string"},
        "yield_note": {"type": "string"},  # выход: «≈20 шариков по 30 г»
        "base_ingredients": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["name", "amount", "note"],
                "additionalProperties": False,
            },
        },
        "ingredients": {"type": "array", "items": _ingredient},
        "steps": {"type": "array", "minItems": 1, "items": _step},
        "notes": {"type": "array", "items": {"type": "string"}},  # общие оговорки точности
    },
    "required": ["lang", "dish", "yield_note", "base_ingredients", "ingredients", "steps"],
    "additionalProperties": False,
}

_validator = Draft202012Validator(ANALYSIS_SCHEMA)


def validate_analysis(data: dict) -> list[str]:
    """Вернуть список ошибок валидации (пустой список — данные корректны)."""
    return [
        f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
        for e in _validator.iter_errors(data)
    ]
