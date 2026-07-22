"""Рендер разбора рецепта: тёмная «кухонная» тема, две панели.

Контракт для streamlit_app.py:
  inject_css()               — вызвать один раз в начале скрипта;
  render_analysis(data, lang) — отрисовать весь разбор (данные уже валидированы
                                по schema.ANALYSIS_SCHEMA и приходят на языке lang).
"""

import html

import streamlit as st

try:
    from app.i18n import ACCURACY_MARKS, NECESSITY_LABELS, t
    from app.schema import COLUMNS
except ImportError:  # запуск скрипта из каталога app/
    from i18n import ACCURACY_MARKS, NECESSITY_LABELS, t
    from schema import COLUMNS

# Палитра тёмной кухонной темы (из скилла cooking-visualizer)
PAL = {
    "bg": "#1a1610",
    "surface": "#242018",
    "card": "#2e2820",
    "border": "#3d3428",
    "gold": "#c8a96e",
    "goldLight": "#e0c48a",
    "goldDim": "#8a7040",
    "red": "#c05040",
    "amber": "#d4904a",
    "green": "#6a9e6e",
    "blue": "#5a8aaa",
    "text": "#f0e8d8",
    "textDim": "#9a8a6a",
}

# Подсветка колонок матрицы (порядок фиксирован schema.COLUMNS):
# 0 — красноватый, ½× — холодный, ¾×/⁵⁄₄× — мягкий амбер (околонормовая зона),
# 1× — золотая рамка и тёплый фон, 3/2× — амбер насыщеннее (дальше от нормы)
_COL_STYLE = {
    "0": "background:rgba(192,80,64,.15);",
    "½×": "background:rgba(90,138,170,.10);",
    "¾×": "background:rgba(212,144,74,.12);",
    "1×": "background:rgba(200,169,110,.14);border:2px solid #c8a96e;",
    "⁵⁄₄×": "background:rgba(212,144,74,.12);",
    "3/2×": "background:rgba(212,144,74,.20);",
}

_CSS = """
<style>
.stApp {
    background: #1a1610;
    color: #f0e8d8;
    font-family: Georgia, "Times New Roman", serif;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
    font-family: Georgia, "Times New Roman", serif;
    color: #e0c48a;
}
.stApp p, .stApp li, .stApp label, .stApp button, .stApp summary,
.stApp input, .stApp textarea, .stApp [data-testid="stMarkdownContainer"] {
    font-family: Georgia, "Times New Roman", serif;
}
[data-testid="stSidebar"] { background: #242018; }
[data-testid="stExpander"] {
    background: #242018;
    border: 1px solid #3d3428;
    border-radius: 8px;
}
[data-testid="stExpander"] summary { color: #f0e8d8; }
[data-testid="stExpander"] summary:hover { color: #e0c48a; }
.stTabs [data-baseweb="tab"] {
    font-family: Georgia, "Times New Roman", serif;
    color: #9a8a6a;
}
.stTabs [aria-selected="true"] { color: #c8a96e; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #c8a96e; }

.cv-yield { color: #9a8a6a; margin: -6px 0 14px; }
.cv-base-card {
    background: #2e2820;
    border: 1px solid #c8a96e;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 14px;
}
.cv-base-title {
    color: #c8a96e;
    font-size: .85em;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.cv-base-row { margin: 6px 0; }
.cv-base-name { color: #e0c48a; font-weight: bold; }
.cv-base-note { color: #9a8a6a; font-size: .85em; }

.cv-cond-note {
    background: rgba(212,144,74,.12);
    border-left: 3px solid #d4904a;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 12px;
    color: #f0e8d8;
    font-size: .92em;
}

.cv-matrix-wrap { overflow-x: auto; margin-bottom: 10px; }
.cv-matrix { border-collapse: collapse; width: 100%; min-width: 560px; }
.cv-matrix th {
    color: #9a8a6a;
    font-weight: normal;
    font-size: .82em;
    text-align: center;
    border-bottom: 1px solid #3d3428;
    padding: 4px 8px;
}
.cv-matrix td {
    border: 1px solid #3d3428;
    padding: 7px 9px;
    vertical-align: top;
    min-width: 88px;
}
/* «мостик» зоны толерантности: общая рамка снизу goldDim у соседних in_zone-ячеек */
.cv-matrix td.cv-zone { border-bottom: 3px solid #8a7040; }
.cv-verdict { color: #f0e8d8; font-size: .9em; }
.cv-conseq { color: #9a8a6a; font-size: .78em; line-height: 1.35; }
.cv-q { color: #d4904a; font-weight: bold; }

.cv-section-title { color: #c8a96e; font-size: .95em; margin: 12px 0 4px; }
.cv-vlist { margin: 0 0 6px; padding-left: 20px; font-size: .9em; color: #f0e8d8; }
.cv-vlist li { margin: 3px 0; }
.cv-vlist b { color: #e0c48a; font-weight: bold; }

.cv-chip {
    display: inline-block;
    background: #2e2820;
    border: 1px solid #3d3428;
    border-radius: 12px;
    padding: 2px 12px;
    margin: 6px 6px 6px 0;
    font-size: .85em;
    color: #e0c48a;
}
.cv-done {
    background: rgba(106,158,110,.15);
    border-left: 3px solid #6a9e6e;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: .92em;
}
.cv-skip {
    background: rgba(192,80,64,.12);
    border-left: 3px solid #c05040;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: .92em;
}
.cv-calib {
    border: 1px solid #d4904a;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: .92em;
}
.cv-block-label { color: #e0c48a; font-weight: bold; }
.cv-dim { color: #9a8a6a; font-size: .82em; margin-top: 6px; }
</style>
"""


def inject_css() -> None:
    """Вставить кастомный CSS. Вызывается один раз в начале streamlit_app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)


def _esc(value) -> str:
    """Экранировать данные перед вставкой в HTML."""
    return html.escape(str(value), quote=True)


def _accuracy_mark(code: str | None) -> str:
    """Метка точности для UI: verified — без метки, estimated — ~, empirical — ?."""
    if not code or code == "verified":
        return ""
    return ACCURACY_MARKS.get(code, "")


def _matrix_html(matrix: list[dict]) -> str:
    """HTML-таблица 6-колоночной матрицы количества."""
    heads = "".join(f"<th>{_esc(col)}</th>" for col in COLUMNS)
    verdicts, conseqs = [], []
    for col, cell in zip(COLUMNS, matrix):
        style = _COL_STYLE[col]
        zone = " cv-zone" if cell.get("in_zone") else ""
        q = ' <span class="cv-q">?</span>' if cell.get("empirical") else ""
        verdicts.append(
            f'<td style="{style}"><span class="cv-verdict">{_esc(cell["verdict"])}{q}</span></td>'
        )
        conseqs.append(
            f'<td class="{zone.strip()}" style="{style}">'
            f'<span class="cv-conseq">{_esc(cell["consequence"])}</span></td>'
        )
    return (
        '<div class="cv-matrix-wrap"><table class="cv-matrix">'
        f"<tr>{heads}</tr>"
        f'<tr>{"".join(verdicts)}</tr>'
        f'<tr>{"".join(conseqs)}</tr>'
        "</table></div>"
    )


def _pairs_html(title: str, items: list[dict]) -> str:
    """Секция «title — detail» для вариантов формы и замен."""
    rows = "".join(
        f'<li><b>{_esc(it["title"])}</b> — {_esc(it["detail"])}</li>' for it in items
    )
    return f'<div class="cv-section-title">{_esc(title)}</div><ul class="cv-vlist">{rows}</ul>'


def _render_ingredients(data: dict, lang: str) -> None:
    """Панель 1: карточка основы + разворачиваемые ингредиенты с матрицей."""
    labels = NECESSITY_LABELS.get(lang, NECESSITY_LABELS["ru"])

    base_rows = "".join(
        f'<div class="cv-base-row">'
        f'<span class="cv-base-name">{_esc(b["name"])}</span> — {_esc(b["amount"])}'
        f'<div class="cv-base-note">{_esc(b["note"])}</div></div>'
        for b in data["base_ingredients"]
    )
    st.markdown(
        f'<div class="cv-base-card">'
        f'<div class="cv-base-title">{_esc(t(lang, "base_card_title"))}</div>'
        f"{base_rows}</div>",
        unsafe_allow_html=True,
    )

    expand_all = st.toggle(t(lang, "expand_all"), key="cv_expand_ingredients")

    for ing in data["ingredients"]:
        # HTML в label expander'а не работает — бейдж необходимости текстом
        label = f'{ing["name"]} · {labels[ing["necessity"]]} · {ing["amount"]}'
        with st.expander(label, expanded=expand_all):
            if ing["necessity"] == "conditional" and ing.get("necessity_note"):
                st.markdown(
                    f'<div class="cv-cond-note">{_esc(ing["necessity_note"])}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(_matrix_html(ing["matrix"]), unsafe_allow_html=True)
            if ing.get("variants"):
                st.markdown(
                    _pairs_html(t(lang, "variants_title"), ing["variants"]),
                    unsafe_allow_html=True,
                )
            if ing.get("substitutions"):
                st.markdown(
                    _pairs_html(t(lang, "substitutions_title"), ing["substitutions"]),
                    unsafe_allow_html=True,
                )


def _render_steps(data: dict, lang: str) -> None:
    """Панель 2: вертикальный таймлайн шагов с чипами техники и метками точности."""
    expand_all = st.toggle(t(lang, "expand_all"), key="cv_expand_steps")

    for num, step in enumerate(data["steps"], start=1):
        eq = step["equipment"]
        dur_mark = _accuracy_mark(step["accuracy"])
        duration = f'{step["duration"]} {dur_mark}'.strip()
        label = f'{num}. {step["title"]} · {eq["device"]} · {duration}'

        with st.expander(label, expanded=expand_all):
            st.markdown(f"<div>{_esc(step['what'])}</div>", unsafe_allow_html=True)

            set_mark = _accuracy_mark(eq.get("accuracy"))
            settings = f'{_esc(eq["settings"])}{" " + set_mark if set_mark else ""}'
            st.markdown(
                f'<span class="cv-chip">{_esc(eq["device"])}</span>'
                f'<span class="cv-chip">{settings}</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="cv-done">✓ <span class="cv-block-label">'
                f'{_esc(t(lang, "done_when"))}:</span> {_esc(step["done_when"])}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="cv-skip">⚠ <span class="cv-block-label">'
                f'{_esc(t(lang, "if_skipped"))}:</span> {_esc(step["if_skipped"])}</div>',
                unsafe_allow_html=True,
            )
            if step.get("calibration"):
                st.markdown(
                    f'<div class="cv-calib">~ <span class="cv-block-label">'
                    f'{_esc(t(lang, "calibration_label"))}:</span> '
                    f'{_esc(step["calibration"])}</div>',
                    unsafe_allow_html=True,
                )


def render_analysis(data: dict, lang: str) -> None:
    """Отрисовать весь разбор: заголовок, две панели, легенда точности и заметки."""
    st.markdown(f'## {data["dish"]}')
    st.markdown(
        f'<div class="cv-yield">{_esc(data["yield_note"])}</div>',
        unsafe_allow_html=True,
    )

    tab_ing, tab_steps = st.tabs([t(lang, "tab_ingredients"), t(lang, "tab_steps")])
    with tab_ing:
        _render_ingredients(data, lang)
    with tab_steps:
        _render_steps(data, lang)

    st.markdown(
        f'<div class="cv-dim">{_esc(t(lang, "accuracy_legend"))}</div>',
        unsafe_allow_html=True,
    )
    for note in data.get("notes") or []:
        st.markdown(f'<div class="cv-dim">· {_esc(note)}</div>', unsafe_allow_html=True)
