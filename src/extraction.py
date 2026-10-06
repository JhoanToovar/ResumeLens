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

    return data
