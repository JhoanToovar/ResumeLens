# Professional Profiles and Canonical Vocabulary

This document fixes two things that every later stage depends on: the four profiles ResumeLens recognizes and the list of canonical tokens. The tokens are the output alphabet Γ of the transducers (Stage 2), the input alphabet Σ of the automata (Stage 3) and the skill values accepted by the DSL (Stage 4).

## 1. Profiles

Two profiles come from the assignment. We chose the other two so they overlap as little as possible with the first two. That way a résumé accepted by one profile says something different from a résumé accepted by another.

| Id | Profile | Area | Origin |
|---|---|---|---|
| `FULL_STACK_DEVELOPER` | Full Stack Developer | Software engineering | Assignment |
| `MACHINE_LEARNING_ENGINEER` | Machine Learning Engineer | AI / data | Assignment |
| `DEVOPS_ENGINEER` | DevOps Engineer | Software engineering | Team |
| `DATA_ENGINEER` | Data Engineer | AI / data | Team |

The assignment says the detailed requirements for the team profiles will be given separately. The two team profiles below are our proposal and will be adjusted if those requirements change them.

### 1.1 Full Stack Developer

Builds the client and server sides of web applications: interfaces, backend services, APIs and database access.

| Order | Group | Tokens | Rule |
|---|---|---|---|
| 1 | Web language | `JAVASCRIPT`, `TYPESCRIPT` | at least one |
| 2 | Frontend framework | `REACT`, `ANGULAR`, `VUE` | at least one |
| 3 | Backend technology | `NODE_JS`, `EXPRESS`, `DJANGO`, `FLASK`, `SPRING_BOOT` | at least one |
| 4 | API style | `REST_API`, `GRAPHQL` | optional |
| 5 | Database | `SQL`, `POSTGRESQL`, `MYSQL`, `SQL_SERVER`, `SQLITE`, `MONGODB`, `REDIS` | at least one |
| 6 | Version control | `GIT` | required |

Check with the assignment example: `JS, React.js, NodeJS, Postgres, Git` becomes `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT`, which covers groups 1, 2, 3, 5 and 6. Accepted.

### 1.2 Machine Learning Engineer

Builds software that trains and serves predictive models, from data processing to model development.

| Order | Group | Tokens | Rule |
|---|---|---|---|
| 1 | Language | `PYTHON` | required |
| 2 | Data library | `PANDAS`, `NUMPY` | at least one |
| 3 | ML library | `SCIKIT_LEARN`, `TENSORFLOW`, `PYTORCH`, `KERAS` | at least one |
| 4 | ML practice | `MACHINE_LEARNING` | optional |
| 5 | SQL | `SQL`, `POSTGRESQL`, `MYSQL`, `SQL_SERVER`, `SQLITE` | optional |
| 6 | Version control | `GIT` | required |

Check with the assignment example: `PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT` covers groups 1, 2, 3, 5 and 6. Accepted.

SQL is optional here because the statement lists it as a possible qualification and the core of the role is the model work. It still counts when present.

### 1.3 DevOps Engineer (team profile, software engineering)

Automates the build, test and deployment of software and keeps the infrastructure running.

| Order | Group | Tokens | Rule |
|---|---|---|---|
| 1 | Scripting | `BASH`, `PYTHON` | optional |
| 2 | Operating system | `LINUX` | required |
| 3 | Containers | `DOCKER` | required |
| 4 | Container orchestration | `KUBERNETES` | optional |
| 5 | CI/CD | `JENKINS`, `GITHUB_ACTIONS`, `GITLAB_CI` | at least one |
| 6 | Cloud | `AWS`, `AZURE`, `GCP` | at least one |
| 7 | Infrastructure as code | `TERRAFORM`, `ANSIBLE` | optional |
| 8 | Version control | `GIT` | required |

Example: `Linux, Docker, K8s, Jenkins, AWS, Terraform, Git` becomes `LINUX, DOCKER, KUBERNETES, JENKINS, AWS, TERRAFORM, GIT`. Accepted.

### 1.4 Data Engineer (team profile, AI/data)

Builds the pipelines that move and transform data so analysts and ML engineers can use it.

| Order | Group | Tokens | Rule |
|---|---|---|---|
| 1 | Language | `PYTHON`, `SCALA`, `JAVA` | at least one |
| 2 | SQL | `SQL`, `POSTGRESQL`, `MYSQL`, `SQL_SERVER`, `SQLITE` | at least one |
| 3 | Distributed processing | `APACHE_SPARK`, `HADOOP` | at least one |
| 4 | Workflow orchestration | `AIRFLOW` | required |
| 5 | Streaming | `KAFKA` | optional |
| 6 | Data warehouse | `SNOWFLAKE`, `BIGQUERY`, `REDSHIFT` | optional |
| 7 | Cloud | `AWS`, `AZURE`, `GCP` | optional |
| 8 | Version control | `GIT` | required |

Example: `Python, SQL, PySpark, Apache Airflow, Kafka, BigQuery, Git` becomes `PYTHON, SQL, APACHE_SPARK, AIRFLOW, KAFKA, BIGQUERY, GIT`. Accepted.

A Machine Learning Engineer résumé like the one in the assignment is rejected here, since it has no Spark and no Airflow.

## 2. Canonical vocabulary

Naming rule: uppercase letters, digits and underscores, starting with a letter. The same rule will be the lexical rule for skills in the DSL, so a token that passes Stage 2 is always a valid DSL value.

The variants column lists the surface forms the transducers must map to each token. Matching is case-insensitive unless the table says otherwise.

| Token | Group | Variants |
|---|---|---|
| `JAVASCRIPT` | Language | JavaScript, Javascript, JS, ECMAScript |
| `TYPESCRIPT` | Language | TypeScript, Typescript, TS |
| `PYTHON` | Language | Python, Python3, Python 3 |
| `JAVA` | Language | Java (not followed by "Script") |
| `SCALA` | Language | Scala |
| `BASH` | Language | Bash, Shell scripting, Shell |
| `SQL` | Language | SQL, T-SQL, PL/SQL |
| `REACT` | Frontend | React, React.js, ReactJS, React JS |
| `ANGULAR` | Frontend | Angular, AngularJS, Angular.js |
| `VUE` | Frontend | Vue, Vue.js, VueJS |
| `NODE_JS` | Backend | Node, NodeJS, Node.js, Node JS |
| `EXPRESS` | Backend | Express, Express.js, ExpressJS |
| `DJANGO` | Backend | Django |
| `FLASK` | Backend | Flask |
| `SPRING_BOOT` | Backend | Spring Boot, SpringBoot, Spring-Boot |
| `REST_API` | API | REST, RESTful, REST API, REST APIs, RESTful API |
| `GRAPHQL` | API | GraphQL, Graph QL |
| `POSTGRESQL` | SQL database | PostgreSQL, Postgres, Postgre, PSQL |
| `MYSQL` | SQL database | MySQL, My SQL |
| `SQL_SERVER` | SQL database | SQL Server, MS SQL Server, MSSQL |
| `SQLITE` | SQL database | SQLite, SQLite3 |
| `MONGODB` | NoSQL database | MongoDB, Mongo, Mongo DB |
| `REDIS` | NoSQL database | Redis |
| `GIT` | Version control | Git |
| `PANDAS` | Data library | Pandas |
| `NUMPY` | Data library | NumPy, Numpy |
| `SCIKIT_LEARN` | ML library | Scikit-learn, scikit learn, sklearn, SciKit-Learn |
| `TENSORFLOW` | ML library | TensorFlow, Tensor Flow, TF2 |
| `PYTORCH` | ML library | PyTorch, Py Torch, Torch |
| `KERAS` | ML library | Keras |
| `MACHINE_LEARNING` | ML practice | Machine Learning, ML, machine-learning model development |
| `LINUX` | Operating system | Linux, GNU/Linux, Ubuntu |
| `DOCKER` | Containers | Docker |
| `KUBERNETES` | Container orchestration | Kubernetes, K8s |
| `JENKINS` | CI/CD | Jenkins |
| `GITHUB_ACTIONS` | CI/CD | GitHub Actions, GH Actions |
| `GITLAB_CI` | CI/CD | GitLab CI, GitLab CI/CD |
| `AWS` | Cloud | AWS, Amazon Web Services |
| `AZURE` | Cloud | Azure, Microsoft Azure |
| `GCP` | Cloud | GCP, Google Cloud, Google Cloud Platform |
| `TERRAFORM` | Infrastructure as code | Terraform |
| `ANSIBLE` | Infrastructure as code | Ansible |
| `APACHE_SPARK` | Distributed processing | Spark, Apache Spark, PySpark |
| `HADOOP` | Distributed processing | Hadoop, Apache Hadoop |
| `AIRFLOW` | Workflow orchestration | Airflow, Apache Airflow |
| `KAFKA` | Streaming | Kafka, Apache Kafka |
| `SNOWFLAKE` | Data warehouse | Snowflake |
| `BIGQUERY` | Data warehouse | BigQuery, Big Query |
| `REDSHIFT` | Data warehouse | Redshift, Amazon Redshift |

Total: 49 tokens. Some come from the assignment examples, but the variant lists are ours, as the statement asks.

## 3. Candidate data outside the vocabulary

Stage 1 also extracts data that is not a qualification token. It does not go through the transducers or the automata. It goes straight to the DSL in Stage 4.

| Field | Example |
|---|---|
| Full name | Wednesday Addams |
| Email | wednesday.addams@nevermore.edu |
| Phone | +57 300 123 4567 |
| Profile URL | linkedin.com/in/..., github.com/... |
| Education | B.Sc. in Systems Engineering, Universidad Icesi, 2024 |
| Experience | 3 years of experience developing web applications |

## 4. Decisions

1. One vocabulary for the whole system. All four profiles read the same tokens, so the pipeline is the same code with a different profile table.
2. Before each automaton runs, the normalized tokens are filtered to the ones in that profile's table, duplicates are removed and the rest is sorted by the Order column. That is how the canonical ordering from the assignment is applied, and it keeps each automaton's alphabet small.
3. A résumé is checked against the four profiles and can be accepted by any number of them, from none to four. The DSL keeps one result per accepted profile.
4. Only qualifications written in the résumé count. Django does not imply Python and TensorFlow does not imply Machine Learning.
5. Ambiguous short variants (`TS`, `ML`, `Node`, `Torch`, `Shell`) are only normalized when Stage 1 found them inside a skills list, never in free text. This rule will be handled when the regexes are written.
