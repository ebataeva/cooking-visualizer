"""Локализация интерфейса Cooking Visualizer (ru / en / es).

Данные разбора приходят уже на нужном языке — здесь только строки UI
и подписи канонических кодов из schema.py (necessity, accuracy).
"""

STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "app_title": "Cooking Visualizer",
        "app_subtitle": "Разбор рецепта: ингредиенты, пропорции и этапы с честными метками точности",
        "recipe_label": "Рецепт",
        "recipe_placeholder": "Вставьте текст рецепта или просто опишите блюдо…",
        "analyze_btn": "Разобрать рецепт",
        "demo_btn": "Демо: фалафель",
        "demo_sushi_rice_btn": "Рис для суши",
        "demo_philadelphia_btn": "Роллы «Филадельфия»",
        "spinner_analyzing": "DeepSeek разбирает рецепт — это займёт около минуты…",
        "tab_ingredients": "Ингредиенты",
        "tab_steps": "Этапы приготовления",
        "expand_all": "Развернуть все",
        "base_card_title": "Основа блюда",
        "variants_title": "Варианты формы",
        "substitutions_title": "Замены",
        "done_when": "Готово, когда",
        "if_skipped": "Если пропустить",
        "calibration_label": "Калибровка первой партии",
        "step_word": "Шаг",
        "err_no_key": "Ключ DeepSeek не найден. Введите его в сайдбаре "
                      "или добавьте в secrets (.streamlit/secrets.toml).",
        "err_api": "Не удалось получить ответ от DeepSeek API. "
                   "Проверьте ключ и соединение, затем повторите попытку.",
        "err_invalid_json": "Модель вернула некорректный JSON — разбор не прошёл валидацию. "
                            "Запустите анализ ещё раз.",
        "key_input_label": "API-ключ DeepSeek",
        "key_input_help": "Ключ используется только в текущей сессии и никуда не сохраняется.",
        "accuracy_legend": "✓ проверено · ~ оценка · ? подбирается опытным путём",
    },
    "en": {
        "app_title": "Cooking Visualizer",
        "app_subtitle": "Recipe breakdown: ingredients, proportions and steps with honest accuracy labels",
        "recipe_label": "Recipe",
        "recipe_placeholder": "Paste a recipe or simply describe the dish…",
        "analyze_btn": "Analyze recipe",
        "demo_btn": "Demo: falafel",
        "demo_sushi_rice_btn": "Sushi rice",
        "demo_philadelphia_btn": "Philadelphia rolls",
        "spinner_analyzing": "DeepSeek is analyzing the recipe — this takes about a minute…",
        "tab_ingredients": "Ingredients",
        "tab_steps": "Cooking steps",
        "expand_all": "Expand all",
        "base_card_title": "Base of the dish",
        "variants_title": "Form variants",
        "substitutions_title": "Substitutions",
        "done_when": "Done when",
        "if_skipped": "If skipped",
        "calibration_label": "First-batch calibration",
        "step_word": "Step",
        "err_no_key": "DeepSeek API key not found. Enter it in the sidebar "
                      "or add it to secrets (.streamlit/secrets.toml).",
        "err_api": "Could not get a response from the DeepSeek API. "
                   "Check your key and connection, then try again.",
        "err_invalid_json": "The model returned invalid JSON — the analysis failed validation. "
                            "Please run the analysis again.",
        "key_input_label": "DeepSeek API key",
        "key_input_help": "The key is used only for this session and is never stored.",
        "accuracy_legend": "✓ verified · ~ estimate · ? found by trial in your kitchen",
    },
    "es": {
        "app_title": "Cooking Visualizer",
        "app_subtitle": "Análisis de la receta: ingredientes, proporciones y pasos con etiquetas honestas de precisión",
        "recipe_label": "Receta",
        "recipe_placeholder": "Pega una receta o simplemente describe el plato…",
        "analyze_btn": "Analizar receta",
        "demo_btn": "Demo: falafel",
        "demo_sushi_rice_btn": "Arroz para sushi",
        "demo_philadelphia_btn": "Rollos Philadelphia",
        "spinner_analyzing": "DeepSeek está analizando la receta — tardará alrededor de un minuto…",
        "tab_ingredients": "Ingredientes",
        "tab_steps": "Pasos de preparación",
        "expand_all": "Expandir todo",
        "base_card_title": "Base del plato",
        "variants_title": "Variantes de forma",
        "substitutions_title": "Sustituciones",
        "done_when": "Está listo cuando",
        "if_skipped": "Si se omite",
        "calibration_label": "Calibración de la primera tanda",
        "step_word": "Paso",
        "err_no_key": "No se encontró la clave de DeepSeek. Introdúcela en la barra lateral "
                      "o añádela a secrets (.streamlit/secrets.toml).",
        "err_api": "No se pudo obtener respuesta de la API de DeepSeek. "
                   "Comprueba la clave y la conexión e inténtalo de nuevo.",
        "err_invalid_json": "El modelo devolvió un JSON no válido — el análisis no pasó la validación. "
                            "Vuelve a ejecutar el análisis.",
        "key_input_label": "Clave API de DeepSeek",
        "key_input_help": "La clave se usa solo en esta sesión y no se guarda en ningún sitio.",
        "accuracy_legend": "✓ verificado · ~ estimación · ? se ajusta con la práctica",
    },
}

# Локализованные бейджи необходимости (коды из schema.NECESSITY)
NECESSITY_LABELS: dict[str, dict[str, str]] = {
    "ru": {
        "base": "ОСНОВА",
        "important": "ВАЖНО",
        "optional": "ОПЦИОНАЛЬНО",
        "conditional": "УСЛОВНЫЙ",
    },
    "en": {
        "base": "BASE",
        "important": "IMPORTANT",
        "optional": "OPTIONAL",
        "conditional": "CONDITIONAL",
    },
    "es": {
        "base": "BASE",
        "important": "IMPORTANTE",
        "optional": "OPCIONAL",
        "conditional": "CONDICIONAL",
    },
}

# Метки точности (коды из schema.ACCURACY) — одинаковы для всех языков
ACCURACY_MARKS = {"verified": "✓", "estimated": "~", "empirical": "?"}


def t(lang: str, key: str) -> str:
    """Строка UI для языка; неизвестный язык или ключ — fallback на русский."""
    return STRINGS.get(lang, STRINGS["ru"]).get(key, STRINGS["ru"].get(key, key))
