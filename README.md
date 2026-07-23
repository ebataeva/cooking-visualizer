# Cooking Visualizer 🥘

Streamlit-приложение: вставьте любой рецепт — получите структурированный разбор
по строгим правилам точности.

- **Панель «Ингредиенты»** — уровень необходимости каждого ингредиента
  (ОСНОВА / ВАЖНО / ОПЦИОНАЛЬНО / УСЛОВНЫЙ), 6-колоночная матрица количеств
  (0 | ½× | ¾× | 1× | ⁵⁄₄× | 3/2×) с зонами толерантности, варианты форм и замены.
- **Панель «Этапы приготовления»** — пошаговый таймлайн с настройками техники,
  метками точности (✓ проверено · ~ оценка · ? подбирается опытным путём),
  сенсорными критериями готовности и последствиями пропуска шага.
- **Языки**: русский / English / Español — кнопка-переключатель в шапке.
- Разбор произвольных рецептов — через DeepSeek API; демо-рецепт (фалафель)
  работает без ключа.

## Локальный запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Ключ DeepSeek (для разбора своих рецептов) ищется в порядке:
`.streamlit/secrets.toml` → переменная окружения `DEEPSEEK_API_KEY` →
файл `~/.deepseek_key` → поле ввода в сайдбаре приложения.

## Деплой на Streamlit Community Cloud

1. Зайти на <https://share.streamlit.io> (вход через GitHub).
2. **Create app** → выбрать репозиторий `ebataeva/cooking-visualizer`,
   ветку `main`, entrypoint `streamlit_app.py`.
3. В **Advanced settings → Secrets** вставить:
   ```toml
   DEEPSEEK_API_KEY = "sk-..."
   ```
4. Deploy. Демо-рецепт работает и без секрета; ключ нужен только для
   разбора произвольных рецептов.

## Структура

```
streamlit_app.py     # entrypoint: язык, ввод рецепта, демо
app/schema.py        # JSON-контракт разбора (jsonschema)
app/analyzer.py      # вызов DeepSeek + валидация + retry
app/render.py        # рендер панелей (HTML/CSS)
app/i18n.py          # строки интерфейса ru/en/es
prompts/system.md    # системный промпт для DeepSeek
data/falafel_*.json  # демо-разбор фалафеля на трёх языках
```
