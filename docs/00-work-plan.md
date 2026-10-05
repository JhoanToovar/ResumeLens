# Work Plan

Team: Jhoan Tovar, Pablo, Edwin. Deadline: October 11, 2026.

Each member owns his part from design to code, so the commits show who built what. Stages 2 and 3 stay together because both are built with pyformlang and the automata read exactly what the transducers write. The repository needs at least 10 meaningful commits with 2 hours or more between consecutive commits. The order below already respects that if each person pushes on the day assigned.

## Ownership

| Member | Stages | Also in charge of |
|---|---|---|
| Jhoan | Stage 1: regular expressions. Stage 4: DSL with textX and the visualization | Repository setup |
| Pablo | Stage 2: finite-state transducers and the per-profile sorting. Stage 3: finite automata for the four profiles | Literature review, profiles |
| Edwin | Architecture and module design, test case design | Console program that runs the four stages (`main.py`), research poster |

The presentation is shared. Each member explains the part he built.

## Commit schedule

| # | Member | Commit content |
|---|---|---|
| 1 | Jhoan | Repository structure, README, requirements, AI log (done) |
| 2 | Pablo | Literature review, profiles and canonical vocabulary, this plan |
| 3 | Edwin | `docs/03-architecture.md`: pipeline diagram, modules with inputs and outputs |
| 4 | Jhoan | `docs/04-regex.md`: one regex per information type and the language it recognizes |
| 5 | Pablo | `docs/05-transducers.md`: 7-tuples, diagrams, sorting rule |
| 6 | Jhoan | `docs/07-grammar.md`: EBNF, terminals and non-terminals, structure of the language |
| 7 | Pablo | `docs/06-automata.md`: 5-tuples, automaton type, diagrams, pattern per profile |
| 8 | Edwin | `docs/08-test-cases.md`: test scenarios for every stage and for the full pipeline |
| 9 | Jhoan | `src/extraction.py` and its tests |
| 10 | Pablo | `src/profiles.py`, `src/normalization.py`, sorting and their tests |
| 11 | Pablo | `src/recognition.py` and its tests |
| 12 | Jhoan | `src/profile_dsl.py`, grammar file, HTML output and tests |
| 13 | Edwin | `main.py`: console program that runs the four stages |
| 14 | Edwin | Research poster |
| 15 | All | README final version, AI log, presentation |

## Rules

- Before pushing, check the time of the last commit in the repository. If 2 hours have not passed, wait.
- A commit must add something: a document section, a working module or tests. Renaming a variable does not count.
- Every time someone uses AI, he adds a row to `docs/ai-log.md` with the prompt and the material he gave it.