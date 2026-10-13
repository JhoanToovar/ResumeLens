# ResumeLens

Formal language-based résumé screening. Integrative Task 1, Computación y Estructuras Discretas III, Universidad Icesi, 2026-2.

## Team

- Jhoan Manuel Tovar Rendon - A00408185
- Juan Pablo Martinez Rosero - A00407215
- Jhon Edwin Escudero - A00408255

## Environment

- Python 3
- IDE: Visual Studio Code
- Libraries: see `requirements.txt`

## How to run

```bash
pip install -r requirements.txt
python main.py          # choose a sample résumé or type the path of a .txt file
streamlit run app.py    # web page: choose or paste a résumé and see every stage in the browser
python -m pytest        # runs the tests in tests/
```

The extracted data (JSON) and the HTML page of each candidate are written to `output/`.

## Repository structure
- `main.py` console program that runs the four stages
- `app.py` simple Streamlit web page that runs the same four stages
- `src/extraction.py` Stage 1, regular expressions
- `src/profiles.py` the four profiles
- `src/normalization.py` Stage 2, finite-state transducers and sorting per profile
- `src/recognition.py` Stage 3, finite automata
- `src/profile_dsl.py` and `src/resumelens.tx` Stage 4, textX DSL and HTML output
- `tests/` tests for every stage and for the full pipeline
- `data/resumes/` sample résumés
- `docs/` design documents and AI usage log
- `docs/ResumeLens_poster.pdf` project poster
