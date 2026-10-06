"""
The four profiles of docs/02-profiles-and-vocabulary.md.
Each profile is a list of groups in order: (group name, tokens, rule).
rule is "required", "at_least_one" or "optional".
"""

SQL_TOKENS = ["SQL", "POSTGRESQL", "MYSQL", "SQL_SERVER", "SQLITE"]
CLOUD_TOKENS = ["AWS", "AZURE", "GCP"]

PROFILES = {
    "FULL_STACK_DEVELOPER": [
        ("Web language", ["JAVASCRIPT", "TYPESCRIPT"], "at_least_one"),
        ("Frontend framework", ["REACT", "ANGULAR", "VUE"], "at_least_one"),
        ("Backend technology", ["NODE_JS", "EXPRESS", "DJANGO", "FLASK", "SPRING_BOOT"], "at_least_one"),
        ("API style", ["REST_API", "GRAPHQL"], "optional"),
        ("Database", SQL_TOKENS + ["MONGODB", "REDIS"], "at_least_one"),
        ("Version control", ["GIT"], "required"),
    ],
    "MACHINE_LEARNING_ENGINEER": [
        ("Language", ["PYTHON"], "required"),
        ("Data library", ["PANDAS", "NUMPY"], "at_least_one"),
        ("ML library", ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH", "KERAS"], "at_least_one"),
        ("ML practice", ["MACHINE_LEARNING"], "optional"),
        ("SQL", SQL_TOKENS, "optional"),
        ("Version control", ["GIT"], "required"),
    ],
    "DEVOPS_ENGINEER": [
        ("Scripting", ["BASH", "PYTHON"], "optional"),
        ("Operating system", ["LINUX"], "required"),
        ("Containers", ["DOCKER"], "required"),
        ("Container orchestration", ["KUBERNETES"], "optional"),
        ("CI/CD", ["JENKINS", "GITHUB_ACTIONS", "GITLAB_CI"], "at_least_one"),
        ("Cloud", CLOUD_TOKENS, "at_least_one"),
        ("Infrastructure as code", ["TERRAFORM", "ANSIBLE"], "optional"),
        ("Version control", ["GIT"], "required"),
    ],
    "DATA_ENGINEER": [
        ("Language", ["PYTHON", "SCALA", "JAVA"], "at_least_one"),
        ("SQL", SQL_TOKENS, "at_least_one"),
        ("Distributed processing", ["APACHE_SPARK", "HADOOP"], "at_least_one"),
        ("Workflow orchestration", ["AIRFLOW"], "required"),
        ("Streaming", ["KAFKA"], "optional"),
        ("Data warehouse", ["SNOWFLAKE", "BIGQUERY", "REDSHIFT"], "optional"),
        ("Cloud", CLOUD_TOKENS, "optional"),
        ("Version control", ["GIT"], "required"),
    ],
}

PROFILE_TITLES = {
    "FULL_STACK_DEVELOPER": "Full Stack Developer",
    "MACHINE_LEARNING_ENGINEER": "Machine Learning Engineer",
    "DEVOPS_ENGINEER": "DevOps Engineer",
    "DATA_ENGINEER": "Data Engineer",
}


def profile_order(profile):
    """all the tokens of a profile, row by row, in the order of the table"""
    order = []
    for group_name, tokens, rule in PROFILES[profile]:
        order += tokens
    return order
