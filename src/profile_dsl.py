"""
Stage 4: candidate profile DSL with textX (see docs/07-grammar.md).
"""
import os
import html
from textx import metamodel_from_file, get_location
from textx.exceptions import TextXSemanticError
from src.normalization import sort_for_profile
from src.profiles import PROFILE_TITLES

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "resumelens.tx")
mm = metamodel_from_file(GRAMMAR_FILE)


def check_candidate(candidate):
    """semantic check: every matched token must be listed in skills"""
    for result in candidate.accepted.profiles:
        for token in result.matched:
            if token not in candidate.skills.tokens:
                raise TextXSemanticError(
                    token + " is used in " + result.profile + " but is not listed in skills",
                    **get_location(result))


mm.register_obj_processors({
    'Candidate': check_candidate
})


def quote(text):
    """text as a DSL STRING (double quotes inside are changed to single quotes)"""
    return '"' + str(text).replace('"', "'") + '"'


def to_dsl(data, tokens, results):
    """writes the candidate profile in the DSL from the outputs of stages 1, 2 and 3"""
    lines = []
    name = data["name"] if data["name"] else "Unknown"
    lines.append("candidate " + quote(name) + " {")

    if data["email"] or data["phone"] or data["urls"]:
        lines.append("    contact {")
        if data["email"]:
            lines.append("        email " + data["email"])
        if data["phone"]:
            lines.append("        phone " + data["phone"])
        for url in data["urls"]:
            lines.append("        url " + url)
        lines.append("    }")

    for edu in data["education"]:
        # "B.Sc. in Systems Engineering, Universidad Icesi, 2022"
        parts = []
        for p in edu["line"].split(","):
            if p.strip() != "" and p.strip() != edu["year"]:
                parts.append(p.strip())
        lines.append("    education {")
        lines.append("        degree " + quote(parts[0]))
        if len(parts) > 1:
            lines.append("        institution " + quote(", ".join(parts[1:])))
        if edu["year"]:
            lines.append("        year " + edu["year"])
        lines.append("    }")

    for job in data["jobs"]:
        lines.append("    experience {")
        lines.append("        role " + quote(job["role"]))
        lines.append("        company " + quote(job["company"]))
        lines.append("        period " + job["start"] + " - " + job["end"].lower())
        lines.append("    }")

    for exp in data["experience"]:
        lines.append("    experience {")
        lines.append("        years " + str(exp["years"]))
        if exp["description"]:
            lines.append("        description " + quote(exp["description"]))
        lines.append("    }")

    lines.append("    skills { " + ", ".join(tokens) + " }")

    lines.append("    accepted {")
    for profile, result in results.items():
        if result == "ACCEPTED":
            matched = sort_for_profile(tokens, profile)
            lines.append("        profile " + profile + " : " + ", ".join(matched))
    lines.append("    }")

    lines.append("}")
    return "\n".join(lines)


def validate(dsl_text):
    """returns the textX model; raises TextXSyntaxError or TextXSemanticError if it is not valid"""
    return mm.model_from_str(dsl_text)


def to_html(model):
    """ HTML page of a valid candidate profile"""
    e = html.escape
    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append("<html><head><meta charset='utf-8'><title>" + e(model.name) + "</title>")
    parts.append("<style>"
                 "body{font-family:Arial,sans-serif;max-width:720px;margin:40px auto;color:#222}"
                 "h1{margin-bottom:4px} h2{border-bottom:1px solid #ccc;padding-bottom:4px}"
                 ".tag{display:inline-block;background:#e8eef7;border-radius:4px;padding:3px 8px;margin:3px;font-size:14px}"
                 ".ok{color:#1b7a3a;font-weight:bold}"
                 "</style></head><body>")
    parts.append("<h1>" + e(model.name) + "</h1>")

    if model.contact:
        info = []
        if model.contact.email:
            info.append(e(model.contact.email))
        if model.contact.phone:
            info.append(e(model.contact.phone))
        for url in model.contact.urls:
            info.append(e(url))
        parts.append("<p>" + " | ".join(info) + "</p>")

    if model.education:
        parts.append("<h2>Education</h2><ul>")
        for edu in model.education:
            text = e(edu.degree)
            if edu.institution:
                text += ", " + e(edu.institution)
            if edu.year:
                text += " (" + edu.year + ")"
            parts.append("<li>" + text + "</li>")
        parts.append("</ul>")

    if model.experience:
        parts.append("<h2>Experience</h2><ul>")
        for exp in model.experience:
            text = ""
            if exp.role:
                text += e(exp.role)
            if exp.company:
                text += " at " + e(exp.company)
            if exp.start:
                text += " (" + exp.start + " - " + exp.end + ")"
            if exp.years:
                text += str(exp.years) + " years"
            if exp.description:
                text += " " + e(exp.description)
            parts.append("<li>" + text.strip() + "</li>")
        parts.append("</ul>")

    parts.append("<h2>Skills</h2><p>")
    for token in model.skills.tokens:
        parts.append("<span class='tag'>" + token + "</span>")
    parts.append("</p>")

    parts.append("<h2>Accepted profiles</h2>")
    if model.accepted.profiles:
        for result in model.accepted.profiles:
            parts.append("<p class='ok'>" + PROFILE_TITLES[result.profile] + " (" + result.profile + ")</p><p>")
            for token in result.matched:
                parts.append("<span class='tag'>" + token + "</span>")
            parts.append("</p>")
    else:
        parts.append("<p>No profile accepted</p>")

    parts.append("</body></html>")
    return "\n".join(parts)
