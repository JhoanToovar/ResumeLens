"""
Stage 1: extraction with regular expressions.
One regex per type of information (see docs/04-regex.md).
"""
import re

# ---------- candidate data ----------
NAME = r'^\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s*$'
EMAIL = r'[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}'
PHONE = r'(?:\+\d{1,3}\s?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}'
URL = r'(?:https?://)?(?:www\.)?(?:linkedin\.com/in|github\.com)/[\w-]+'
EDUCATION = r"^.*?(?<!\w)(Bachelor(?:'s)?|Master(?:'s)?|Ph\.?\s?D\.?|B\.?\s?Sc\.?|M\.?\s?Sc\.?)(?!\w).*$"
YEAR = r'\b(?:19|20)\d{2}\b'
EXPERIENCE = r'(\d{1,2})\+?\s+years?\s+of\s+(?:professional\s+)?experience\s*([^.\n]*)'
JOB = r'^\s*(.+?)\s+at\s+(.+?)\s*\((\d{4})\s*-\s*(\d{4}|present)\)'

# ---------- qualifications ----------
SKILLS_SECTION = r'skills\s*:\s*(.+?)(?:\n\s*\n|\Z)'

LEFT = r'(?<![\w.])'   # not glued to a letter, digit or dot on the left
RIGHT = r'(?!\w)'      # not followed by a letter or digit

FRAMEWORKS = LEFT + r'(React(?:\.?\s?JS)?|Angular(?:\.?JS)?|Vue(?:\.?JS)?|Node(?:\.?\s?JS)?|Express(?:\.?JS)?|Django|Flask|Spring[\s-]?Boot|Pandas|NumPy|Scikit[\s-]?learn|sklearn|Tensor\s?Flow|TF2|Py\s?Torch|Torch|Keras|PySpark|Apache\s+Spark|Spark)' + RIGHT
DATABASES = LEFT + r'(PostgreSQL|Postgres|Postgre|PSQL|My\s?SQL|(?:MS\s+)?SQL\s+Server|MSSQL|SQLite3?|Mongo\s?DB|Mongo|Redis|Snowflake|Big\s?Query|(?:Amazon\s+)?Redshift)' + RIGHT
TOOLS = LEFT + r'(GitHub\s+Actions|GH\s+Actions|GitLab\s+CI(?:/CD)?|Git|Docker|Kubernetes|K8s|Jenkins|AWS|Amazon\s+Web\s+Services|(?:Microsoft\s+)?Azure|GCP|Google\s+Cloud(?:\s+Platform)?|Terraform|Ansible|GNU/Linux|Linux|Ubuntu|(?:Apache\s+)?Airflow|(?:Apache\s+)?Kafka|(?:Apache\s+)?Hadoop|RESTful(?:\s+APIs?)?|REST(?:\s+APIs?)?|Graph\s?QL)' + RIGHT

SKILL_PATTERNS = [
    ("frameworks", FRAMEWORKS),
    ("databases", DATABASES),
    ("tools", TOOLS),
]


def extract_skills(text):
    """returns a dict {type: [skills as written]} found in the skills section"""
    section = re.search(SKILLS_SECTION, text, re.IGNORECASE | re.DOTALL)
    rest = section.group(1) if section else ""
    found = {}
    for name, pattern in SKILL_PATTERNS:
        found[name] = re.findall(pattern, rest, re.IGNORECASE)
        # erase what was found so the next pattern does not find it again
        rest = re.sub(pattern, ",", rest, flags=re.IGNORECASE)
    return found


def extract(text):
    """Stage 1: returns a dictionary with the candidate data and the skills"""
    data = {}

    match = re.search(NAME, text, re.MULTILINE)
    data["name"] = match.group(1) if match else None

    match = re.search(EMAIL, text)
    data["email"] = match.group(0) if match else None

    match = re.search(PHONE, text)
    data["phone"] = match.group(0) if match else None

    data["urls"] = re.findall(URL, text, re.IGNORECASE)

    data["education"] = []
    for match in re.finditer(EDUCATION, text, re.MULTILINE):
        line = match.group(0).strip()
        year = re.search(YEAR, line)
        data["education"].append({
            "degree": match.group(1),
            "line": line,
            "year": year.group(0) if year else None,
        })

    data["experience"] = []
    for years, description in re.findall(EXPERIENCE, text, re.IGNORECASE):
        data["experience"].append({"years": int(years), "description": description.strip()})

    data["jobs"] = []
    for role, company, start, end in re.findall(JOB, text, re.MULTILINE | re.IGNORECASE):
        data["jobs"].append({"role": role, "company": company, "start": start, "end": end})

    data["skills_by_type"] = extract_skills(text)
    data["skills"] = []
    for name, _ in SKILL_PATTERNS:
        data["skills"] += data["skills_by_type"][name]

    return data
