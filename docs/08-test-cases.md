# Test Case Design

The tests check each stage alone and then the whole pipeline. Each stage can be tested without the others because its input is plain data (a string or a list), as described in `03-architecture.md`. Every expected result below was checked against prototypes of the stages.

Test files: `tests/test_extraction.py`, `tests/test_normalization.py`, `tests/test_recognition.py`, `tests/test_profile_dsl.py` and `tests/test_pipeline.py`, run with `pytest`.

## 1. Sample résumés

These files go in `data/resumes/`. R1 and R2 come from the assignment. The rest were written by the team to cover the other profiles and the edge cases.

| Id | File | Purpose |
|---|---|---|
| R1 | `wednesday_addams.txt` | Full Stack example from the assignment |
| R2 | `mary_jane_watson.txt` | Machine Learning example from the assignment |
| R3 | `leon_kennedy.txt` | Full Stack with contact data, education, a job and many skill variants |
| R4 | `chris_redfield.txt` | DevOps profile; has data tools but no SQL |
| R5 | `catherine_halsey.txt` | Data Engineer profile |
| R6 | `ada_wong.txt` | accepted by two profiles at once |
| R7 | `jill_valentine.txt` | skills section with nothing technical |
| R8 | `avery_johnson.txt` | no skills section at all |

R3:
```
Leon Kennedy
leon.kennedy@rpd.example.com | +57 300 123 4567 | linkedin.com/in/leon-kennedy
B.Sc. in Systems Engineering, Universidad Icesi, 2022
Backend Developer at Umbrella Corporation (2022 - present)
Skills: TypeScript, React JS, Node.js, Express.js, My SQL, SQL Server, MongoDB, REST APIs, Git, GitHub Actions, Docker, Java, JavaScript, T-SQL, ML, HTML
```

R4:
```
Chris Redfield
5+ years of professional experience in cloud infrastructure
Master's in Computer Science, 2019
Skills: Bash, Linux, Docker, K8s, Jenkins, AWS, Terraform, Git, PySpark, Apache Airflow, Kafka, BigQuery, Python 3, Scala
```

R5:
```
Catherine Halsey
catherine.halsey@oni.example.org
M.Sc. in Data Science, Universidad del Valle, 2021
Data Engineer at Office of Naval Intelligence (2021 - present)
Skills: Python, SQL, PySpark, Apache Airflow, Kafka, Snowflake, AWS, Git
```

R6:
```
Ada Wong
Skills: Python, Pandas, NumPy, Scikit-learn, PySpark, SQL, Apache Airflow, Git, JS, JavaScript
```

R7:
```
Jill Valentine
Police officer with 6 years of experience in special tactics.
Skills: Lockpicking, First aid, Marksmanship
```

R8:
```
Avery Johnson
I have used Python, Pandas and TensorFlow in several projects.
```

## 2. Stage 1: extraction

| Id | Scenario | Input | Expected |
|---|---|---|---|
| E1 | skills from the assignment example | R1 | skills `React.js, NodeJS, Postgres, Git, JS` |
| E2 | all candidate data | R3 | name `Leon Kennedy`, email `leon.kennedy@rpd.example.com`, phone `+57 300 123 4567`, url `linkedin.com/in/leon-kennedy` |
| E3 | education and job | R3 | degree `B.Sc.`, year `2022`; job `Backend Developer`, `Umbrella Corporation`, `2022`, `present` |
| E4 | years of experience | R1 | years `3`, description `developing web applications` |
| E5 | short names inside longer ones | `Skills: React JS, My SQL, SQL Server, T-SQL` | `React JS`, `My SQL`, `SQL Server`, `T-SQL`; no separate `JS` or `SQL` |
| E6 | `Java` next to `JavaScript` | `Skills: Java, JavaScript` | `Java` and `JavaScript`, each once |
| E7 | non-technical skills | R7 | empty skills list |
| E8 | no skills section | R8 | empty skills list, even though the text mentions Python |
| E9 | invalid email | `leon@site` | email `None` |

## 3. Stage 2: normalization and sorting

| Id | Scenario | Input | Expected |
|---|---|---|---|
| N1 | variants from the assignment | `JS`, `React.js`, `NodeJS`, `Postgres` | `JAVASCRIPT`, `REACT`, `NODE_JS`, `POSTGRESQL` |
| N2 | different separators | `Scikit-learn`, `Scikit learn`, `sklearn` | `SCIKIT_LEARN` three times |
| N3 | case does not matter | `NUMPY`, `numpy`, `NumPy` | `NUMPY` |
| N4 | multi-word variant | `GitLab CI/CD`, `Google Cloud Platform` | `GITLAB_CI`, `GCP` |
| N5 | prefix that is not a skill | `Spring` | not recognized |
| N6 | unknown skill | `HTML`, `Reac` | not recognized, listed as unrecognized |
| N7 | repeated skill | `JS`, `JavaScript` | one `JAVASCRIPT` |
| S1 | sorting for Full Stack | `GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT` | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` |
| S2 | filtering for another profile | same tokens, Machine Learning Engineer | `POSTGRESQL, GIT` |
| S3 | no tokens of the profile | `REACT, NODE_JS`, DevOps Engineer | empty list |

## 4. Stage 3: recognition

Inputs are already sorted for the profile.

| Id | Profile | Input | Expected |
|---|---|---|---|
| A1 | Full Stack | `JAVASCRIPT REACT NODE_JS POSTGRESQL GIT` | ACCEPTED |
| A2 | Full Stack | `TYPESCRIPT ANGULAR SPRING_BOOT REST_API MYSQL MONGODB GIT` | ACCEPTED (optional group and two databases) |
| A3 | Full Stack | `JAVASCRIPT REACT POSTGRESQL GIT` | REJECTED (no backend) |
| A4 | ML Engineer | `PYTHON PANDAS TENSORFLOW POSTGRESQL GIT` | ACCEPTED (assignment example) |
| A5 | ML Engineer | `PYTHON PANDAS NUMPY SQL GIT` | REJECTED (no ML library) |
| A6 | DevOps | `BASH LINUX DOCKER GITHUB_ACTIONS AZURE GIT` | ACCEPTED |
| A7 | DevOps | `LINUX DOCKER KUBERNETES AWS GIT` | REJECTED (no CI/CD) |
| A8 | Data Engineer | `SCALA POSTGRESQL HADOOP AIRFLOW AWS GIT` | ACCEPTED |
| A9 | Data Engineer | `PYTHON APACHE_SPARK AIRFLOW KAFKA BIGQUERY GIT` | REJECTED (no SQL) |
| A10 | any | empty sequence | REJECTED |
| A11 | Full Stack | `JAVASCRIPT REACT NODE_JS POSTGRESQL` | REJECTED (ends before Git, not in a final state) |
| A12 | all four | the four automata | `is_deterministic()` is `True` |

## 5. Stage 4: DSL validation and visualization

| Id | Scenario | Input | Expected |
|---|---|---|---|
| D1 | minimal valid profile | Wednesday profile from `07-grammar.md` | parsed, `name` is `Wednesday Addams` |
| D2 | profile with every block | Leon profile from `07-grammar.md` | parsed, 2 urls, education year `2022`, job end `present` |
| D3 | no accepted profile | `accepted { }` | parsed, empty list |
| D4 | lexical error in email | `email leon.kennedy@` | `TextXSyntaxError` |
| D5 | lowercase token | `skills { JAVASCRIPT, react }` | `TextXSyntaxError` |
| D6 | unknown profile name | `profile DATA_SCIENTIST : PYTHON` | `TextXSyntaxError` |
| D7 | blocks in the wrong order | `skills` before `experience` | `TextXSyntaxError` |
| D8 | block not closed | last `}` missing | `TextXSyntaxError` |
| D9 | matched token not in skills | `profile FULL_STACK_DEVELOPER : TYPESCRIPT` with no `TYPESCRIPT` in skills | `TextXSemanticError` |
| D10 | HTML output | D1 model | HTML contains `Wednesday Addams`, the 5 skills and `FULL_STACK_DEVELOPER` |

## 6. Full pipeline

| Id | Résumé | Expected tokens | Expected classification |
|---|---|---|---|
| P1 | R1 | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` | Full Stack ACCEPTED, the rest REJECTED |
| P2 | R2 | `PYTHON, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, SQL, GIT` | ML Engineer ACCEPTED, the rest REJECTED |
| P3 | R3 | 15 tokens; `HTML` is ignored because no pattern matches it | Full Stack ACCEPTED, the rest REJECTED |
| P4 | R4 | 14 tokens | DevOps ACCEPTED; Data Engineer REJECTED (no SQL) |
| P5 | R5 | 8 tokens | Data Engineer ACCEPTED, the rest REJECTED |
| P6 | R6 | 9 tokens, `JS` and `JavaScript` counted once | ML Engineer and Data Engineer ACCEPTED |
| P7 | R7 | none | all REJECTED, valid DSL with `accepted { }` |
| P8 | R8 | none | all REJECTED, valid DSL with `accepted { }` |
| P9 | any of R1 to R8 | | the generated DSL text passes `validate` and an HTML file is written to `output/` |
| P10 | file that does not exist | | error message, the program keeps running |
