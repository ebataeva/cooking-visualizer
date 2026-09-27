"""Cooking Visualizer — разбор рецептов по правилам скилла cooking-visualizer."""

import json
import sys
from pathlib import Path

# каталог проекта в sys.path — для запуска через AppTest и из другого cwd
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from app import analyzer
from app.i18n import t
from app.render import inject_css, render_analysis

DATA_DIR = Path(__file__).parent / "data"
LANG_OPTIONS = ["RU", "EN", "ES"]
# демо-разборы: имя файла data/<name>_<lang>.json → ключ подписи кнопки в i18n
DEMOS = {
    "falafel": "demo_btn",
    "sushi_rice": "demo_sushi_rice_btn",
    "philadelphia_roll": "demo_philadelphia_btn",
}

st.set_page_config(page_title="Cooking Visualizer", page_icon="🥘", layout="wide")

lang = st.session_state.setdefault("lang", "ru")
inject_css()

# шапка: заголовок слева, переключатель языка справа
col_title, col_lang = st.columns([4, 1], vertical_alignment="center")
with col_lang:
    choice = st.segmented_control(
        "lang", LANG_OPTIONS, default=lang.upper(), label_visibility="collapsed"
    )
    if choice and choice.lower() != lang:
        st.session_state.lang = choice.lower()
        st.rerun()
lang = st.session_state.lang
with col_title:
    st.title(t(lang, "app_title"))
    st.caption(t(lang, "app_subtitle"))

# ключ API: если не найден автоматически — поле ввода в сайдбаре
api_key = analyzer.get_api_key()
if not api_key:
    with st.sidebar:
        st.text_input(
            t(lang, "key_input_label"),
            type="password",
            key="user_api_key",
            help=t(lang, "key_input_help"),
        )
    api_key = analyzer.get_api_key()

recipe = st.text_area(
    t(lang, "recipe_label"),
    placeholder=t(lang, "recipe_placeholder"),
    height=180,
)
# кнопки только для демо, у которых есть файл на текущем языке
demos = [name for name in DEMOS if (DATA_DIR / f"{name}_{lang}.json").exists()]
col_run, *demo_cols = st.columns([1] * (len(demos) + 1))
if col_run.button(t(lang, "analyze_btn"), type="primary", disabled=not recipe.strip()):
    st.session_state.analysis_source = ("llm", recipe.strip())
for col, name in zip(demo_cols, demos):
    if col.button(t(lang, DEMOS[name])):
        st.session_state.analysis_source = ("demo", name)

source = st.session_state.get("analysis_source")
if source:
    kind, text = source
    if kind == "demo":
        # после смены языка выбранного демо может не быть — откат на фалафель
        path = DATA_DIR / f"{text}_{lang}.json"
        if not path.exists():
            path = DATA_DIR / f"falafel_{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        render_analysis(data, lang)
    elif not api_key:
        st.error(t(lang, "err_no_key"))
    else:
        try:
            with st.spinner(t(lang, "spinner_analyzing")):
                data = analyzer.analyze(text, lang, api_key)
            render_analysis(data, lang)
        except analyzer.AnalyzerError as e:
            msg = str(e)
            key = "err_invalid_json" if msg.startswith("invalid_json") else "err_api"
            st.error(t(lang, key))
            st.caption(msg[:500])
