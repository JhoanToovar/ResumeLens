# Stage 1: Extraction with Regular Expressions

Stage 1 reads the résumé text and pulls out the pieces the next stages need. It does not decide that `JS` and `JavaScript` are the same (that is Stage 2) and it does not decide if the candidate fits a profile (that is Stage 3). It only finds strings.

All patterns use Python's `re` module, with the same functions we used in Follow-up 1: `re.search`, `re.findall`, `re.finditer`, `re.sub` and the flags `re.IGNORECASE` and `re.MULTILINE`.

## 1. Two kinds of information

| Kind | Types | Where it goes |
|---|---|---|
| Candidate data | name, email, phone, profile URL, education, experience | straight to Stage 4 (DSL) |
| Qualifications | programming languages, frameworks and libraries, databases, tools and technologies, other qualifications | Stage 2 (transducers) |

## 2. Candidate data

### 2.1 Name

```
^\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s*$
```

Recognizes a whole line made of 2 to 4 words, each one starting with an uppercase letter followed by lowercase letters. Accented letters and `Ñ` are included for Spanish names. Used with `re.MULTILINE` so `^` and `$` work per line, and we keep the first match, since the name usually opens the résumé.

| Matches | Does not match |
|---|---|
| `Wednesday Addams`, `Mary Jane Watson`, `José Pérez` | `Technical Skills:` (has a colon), `wednesday addams` (lowercase) |

### 2.2 Email

```
[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}
```

A user part (letters, digits, `_`, `.`, `+`, `-`), one `@`, a domain with optional subdomains, and an ending of at least 2 letters.

| Matches | Does not match |
|---|---|
| `leon.kennedy@rpd.example.com`, `a.b@mail.co` | `leon@site` (no ending), `user@@x.com` |

### 2.3 Phone

```
(?:\+\d{1,3}\s?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}
```

An optional country code (`+` and 1 to 3 digits), then 10 digits split as 3, 3 and 4, with optional spaces, dashes or parentheses around the first group.

| Matches | Does not match |
|---|---|
| `+57 300 123 4567`, `(602) 555-1234`, `300 123 4567` | `2018-2022` (only 8 digits) |

### 2.4 Profile URL

```
(?:https?://)?(?:www\.)?(?:linkedin\.com/in|github\.com)/[\w-]+
```

LinkedIn or GitHub profile links, with or without `https://` and `www.`. Used with `re.findall` because a résumé can have both.

| Matches | Does not match |
|---|---|
| `linkedin.com/in/leon-kennedy`, `https://github.com/lkennedy` | `github.com` (no user) |

### 2.5 Education

```
^.*?(?<!\w)(Bachelor(?:'s)?|Master(?:'s)?|Ph\.?\s?D\.?|B\.?\s?Sc\.?|M\.?\s?Sc\.?)(?!\w).*$
```

A line that contains a degree name. Group 1 is the degree and the whole match is the line, which keeps the field and the institution. A second pattern takes the year from that line:

```
\b(?:19|20)\d{2}\b
```

| Matches | Does not match |
|---|---|
| `B.Sc. in Systems Engineering, Universidad Icesi, 2022` gives degree `B.Sc.`, year `2022` | `Data engineering pipelines` (no degree word) |

### 2.6 Experience

Years of experience written as a sentence:

```
(\d{1,2})\+?\s+years?\s+of\s+(?:professional\s+)?experience\s*([^.\n]*)
```

Group 1 is the number of years and group 2 is the rest of the sentence up to the period.

Jobs written as `Role at Company (start - end)`:

```
^\s*(.+?)\s+at\s+(.+?)\s*\((\d{4})\s*-\s*(\d{4}|present)\)
```

| Matches | Result |
|---|---|
| `3 years of experience developing web applications.` | years `3`, description `developing web applications` |
| `5+ years of professional experience in cloud infrastructure` | years `5`, description `in cloud infrastructure` |
| `Backend Developer at Umbrella Corporation (2022 - present)` | role, company, `2022`, `present` |

## 3. Qualifications

### 3.1 The skills section

Skills are only searched inside the skills section, not in the whole résumé. This avoids false matches like `ML` or `Shell` inside normal sentences. The section starts after `Skills:` (or `Technical Skills:`) and ends at a blank line or at the end of the text:

```
skills\s*:\s*(.+?)(?:\n\s*\n|\Z)
```

Flags: `re.IGNORECASE` and `re.DOTALL`, so the section can span several lines.

### 3.2 Boundaries

Every qualification pattern is wrapped like this:

```
(?<![\w.])( ...alternatives... )(?!\w)
```

The lookbehind says "not glued to a letter, digit or dot on the left", and the lookahead says "not followed by a letter or digit". Without them, `JS` would be found inside `React.js` and `SQL` inside `PostgreSQL`. Both checks look at a single character, so the language of each pattern is still regular: the same check could be drawn as one extra state in an automaton.

### 3.3 One pattern per type

Each pattern is a list of alternatives with `|`, longer forms first, and it is used with `re.findall` and `re.IGNORECASE`. The strings are kept exactly as written, since normalizing them is Stage 2's job.

Frameworks and libraries:
```
React(?:\.?\s?JS)?|Angular(?:\.?JS)?|Vue(?:\.?JS)?|Node(?:\.?\s?JS)?|Express(?:\.?JS)?|Django|Flask|Spring[\s-]?Boot|Pandas|NumPy|Scikit[\s-]?learn|sklearn|Tensor\s?Flow|TF2|Py\s?Torch|Torch|Keras|PySpark|Apache\s+Spark|Spark
```

Databases:
```
PostgreSQL|Postgres|Postgre|PSQL|My\s?SQL|(?:MS\s+)?SQL\s+Server|MSSQL|SQLite3?|Mongo\s?DB|Mongo|Redis|Snowflake|Big\s?Query|(?:Amazon\s+)?Redshift
```

Tools and technologies:
```
GitHub\s+Actions|GH\s+Actions|GitLab\s+CI(?:/CD)?|Git|Docker|Kubernetes|K8s|Jenkins|AWS|Amazon\s+Web\s+Services|(?:Microsoft\s+)?Azure|GCP|Google\s+Cloud(?:\s+Platform)?|Terraform|Ansible|GNU/Linux|Linux|Ubuntu|(?:Apache\s+)?Airflow|(?:Apache\s+)?Kafka|(?:Apache\s+)?Hadoop|RESTful(?:\s+APIs?)?|REST(?:\s+APIs?)?|Graph\s?QL
```

Other qualifications:
```
Machine[\s-]Learning(?:\s+model\s+development)?|ML
```

Programming languages:
```
JavaScript|ECMAScript|JS|TypeScript|TS|Python\s?3|Python|Java|Scala|Bash|Shell(?:\s+scripting)?|T-SQL|PL/SQL|SQL
```

### 3.4 Order

The patterns run in the order above, and each one erases what it found (with `re.sub`) before the next one runs. Languages go last because their short names hide inside other names: `JS` in `React JS`, `SQL` in `My SQL` or `SQL Server`. By the time the language pattern runs, those strings are already gone.

Example with the skills line `TypeScript, React JS, My SQL, SQL Server, Git, GitHub Actions, T-SQL`:

| Pattern | Finds |
|---|---|
| Frameworks | `React JS` |
| Databases | `My SQL`, `SQL Server` |
| Tools | `Git`, `GitHub Actions` |
| Other | nothing |
| Languages | `TypeScript`, `T-SQL` |

## 4. Output

`extract(text)` returns a dictionary. With the Wednesday Addams résumé from the assignment:

```python
{
    "name": "Wednesday Addams",
    "email": None,
    "phone": None,
    "urls": [],
    "education": [],
    "experience": [{"years": 3, "description": "developing web applications"}],
    "jobs": [],
    "skills_by_type": {
        "frameworks": ["React.js", "NodeJS"],
        "databases": ["Postgres"],
        "tools": ["Git"],
        "other": [],
        "languages": ["JS"],
    },
    "skills": ["React.js", "NodeJS", "Postgres", "Git", "JS"],
}
```

`skills` is the list Stage 2 receives. The order does not matter, because Stage 2 sorts the tokens per profile anyway. The dictionary can also be saved as JSON in `output/`, which covers the requirement of keeping the extracted information in a file or a data structure.

## 5. Limitations

- Only skills listed under a `Skills:` heading are found. A skill mentioned only in a sentence ("built APIs with Django") is missed.
- A skill written in a way not listed in the patterns is not found. Adding it means adding an alternative to the right pattern and to the transducers.
- The name pattern expects each word to start with one uppercase letter, so `McDonald` or `de la Cruz` are not recognized as names.
- Résumés in Spanish are out of scope: the degree and experience patterns use English words.
