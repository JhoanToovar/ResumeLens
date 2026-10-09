## Team

- Jhoan Manuel Tovar Rendon - A00408185
- Juan Pablo Martinez Rosero - A00407215
- Jhon Edwin Escudero - A00408255

````markdown
## How to run

```bash
pip install -r requirements.txt
python main.py          # choose a sample résumé or type the path of a .txt file
python -m pytest        # runs the tests in tests/
```

The extracted data (JSON) and the HTML page of each candidate are written to `output/`.

## Repository structure
- `main.py` console program that runs the four stages
- `src/extraction.py` Stage 1, regular expressions
- `src/profiles.py` the four profiles
- `src/normalization.py` Stage 2, finite-state transducers and sorting per profile
- `src/recognition.py` Stage 3, finite automata
- `src/profile_dsl.py` and `src/resumelens.tx` Stage 4, textX DSL and HTML output
- `tests/` tests for every stage and for the full pipeline
- `data/resumes/` sample résumés
- `docs/` design documents and AI usage log
````
