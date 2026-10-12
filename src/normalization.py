"""
Normalization with finite-state transducers.
Five transducers, one per skill type found in Stage 1.
"""
import re
from pyformlang.fst import FST
from src.profiles import profile_order

END = "#"   # end mark: the token is written only when the skill is over

# canonical token -> variants, one table per transducer
VARIANTS = {
    "T_LANG": {
        "JAVASCRIPT": ["JavaScript", "JS", "ECMAScript"],
        "TYPESCRIPT": ["TypeScript", "TS"],
        "PYTHON": ["Python", "Python3", "Python 3"],
        "JAVA": ["Java"],
        "SCALA": ["Scala"],
        "BASH": ["Bash", "Shell", "Shell scripting"],
        "SQL": ["SQL", "T-SQL", "PL/SQL"],
    },
    "T_FW": {
        "REACT": ["React", "React.js", "ReactJS", "React JS"],
        "ANGULAR": ["Angular", "AngularJS", "Angular.js"],
        "VUE": ["Vue", "Vue.js", "VueJS"],
        "NODE_JS": ["Node", "NodeJS", "Node.js", "Node JS"],
        "EXPRESS": ["Express", "Express.js", "ExpressJS"],
        "DJANGO": ["Django"],
        "FLASK": ["Flask"],
        "SPRING_BOOT": ["Spring Boot", "SpringBoot", "Spring-Boot"],
        "PANDAS": ["Pandas"],
        "NUMPY": ["NumPy"],
        "SCIKIT_LEARN": ["Scikit-learn", "Scikit learn", "Scikitlearn", "sklearn"],
        "TENSORFLOW": ["TensorFlow", "Tensor Flow", "TF2"],
        "PYTORCH": ["PyTorch", "Py Torch", "Torch"],
        "KERAS": ["Keras"],
        "APACHE_SPARK": ["Spark", "Apache Spark", "PySpark"],
    },
    "T_DB": {
        "POSTGRESQL": ["PostgreSQL", "Postgres", "Postgre", "PSQL"],
        "MYSQL": ["MySQL", "My SQL"],
        "SQL_SERVER": ["SQL Server", "MS SQL Server", "MSSQL"],
        "SQLITE": ["SQLite", "SQLite3"],
        "MONGODB": ["MongoDB", "Mongo DB", "Mongo"],
        "REDIS": ["Redis"],
        "SNOWFLAKE": ["Snowflake"],
        "BIGQUERY": ["BigQuery", "Big Query"],
        "REDSHIFT": ["Redshift", "Amazon Redshift"],
    },
    "T_TOOL": {
        "GIT": ["Git"],
        "DOCKER": ["Docker"],
        "KUBERNETES": ["Kubernetes", "K8s"],
        "JENKINS": ["Jenkins"],
        "GITHUB_ACTIONS": ["GitHub Actions", "GH Actions"],
        "GITLAB_CI": ["GitLab CI", "GitLab CI/CD"],
        "AWS": ["AWS", "Amazon Web Services"],
        "AZURE": ["Azure", "Microsoft Azure"],
        "GCP": ["GCP", "Google Cloud", "Google Cloud Platform"],
        "TERRAFORM": ["Terraform"],
        "ANSIBLE": ["Ansible"],
        "LINUX": ["Linux", "GNU/Linux", "Ubuntu"],
        "AIRFLOW": ["Airflow", "Apache Airflow"],
        "KAFKA": ["Kafka", "Apache Kafka"],
        "HADOOP": ["Hadoop", "Apache Hadoop"],
        "REST_API": ["REST", "RESTful", "REST API", "REST APIs", "RESTful API", "RESTful APIs"],
        "GRAPHQL": ["GraphQL", "Graph QL"],
    },
    "T_OTHER": {
        "MACHINE_LEARNING": ["Machine Learning", "Machine-Learning", "ML",
                             "Machine Learning model development", "Machine-learning model development"],
    },
}


def to_symbols(raw):
    """lowercase, split on spaces, dots, dashes and slashes, add the end mark.
    'React.js' -> ['react', 'js', '#']"""
    words = re.split(r"[\s.\-/]+", raw.lower())
    symbols = []
    for w in words:
        if w != "":
            symbols.append(w)
    symbols.append(END)
    return symbols


def state_name(words, sequences):
    """state reached after reading `words`.
    A complete variant that no longer variant continues ends in the token state (q_REACT).
    Otherwise the state is named with the words read so far (q_react)."""
    longer = False
    for s in sequences:
        if len(s) > len(words) and s[:len(words)] == words:
            longer = True
    if words in sequences and not longer:
        return "q_" + sequences[words]
    return "q_" + "_".join(words)


def transitions(table):
    """rows (state, input word, next state, output) of one transducer"""
    sequences = {}
    for token, variants in table.items():
        for v in variants:
            sequences[tuple(to_symbols(v)[:-1])] = token

    rows = []
    seen = []
    for words, token in sequences.items():
        state = "q0"
        for i in range(len(words)):
            next_state = state_name(words[:i + 1], sequences)
            if (state, words[i]) not in seen:
                seen.append((state, words[i]))
                rows.append((state, words[i], next_state, []))# writes epsilon
            state = next_state
        if (state, END) not in seen:
            seen.append((state, END))
            rows.append((state, END, "qf", [token]))# writes the token
    return rows


def build_transducer(table):
    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state("qf")
    for state, word, next_state, output in transitions(table):
        fst.add_transition(state, word, next_state, output)
    return fst


TRANSDUCERS = {}
for name, table in VARIANTS.items():
    TRANSDUCERS[name] = build_transducer(table)


def normalize_skill(raw):
    """returns the canonical token of one skill, or None if no transducer accepts it"""
    symbols = to_symbols(raw)
    for name, fst in TRANSDUCERS.items():
        result = list(fst.translate(symbols))
        if result:
            return result[0][0]
    return None


def normalize(skills):
    """list of skills as written -> list of canonical tokens without repeats"""
    tokens = []
    for raw in skills:
        token = normalize_skill(raw)
        if token is None:
            print("Warning: skill not recognized:", raw)
        elif token not in tokens:
            tokens.append(token)
    return tokens


def unrecognized(skills):
    """skills that no transducer accepts"""
    result = []
    for raw in skills:
        if normalize_skill(raw) is None:
            result.append(raw)
    return result


def sort_for_profile(tokens, profile):
    """keeps the tokens of the profile, without repeats, in the profile order"""
    order = profile_order(profile)
    result = []
    for token in order:
        if token in tokens and token not in result:
            result.append(token)
    return result
