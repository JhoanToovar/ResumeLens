"""
Stage 4: candidate profile DSL with textX (see docs/07-grammar.md).
"""
import os
from textx import metamodel_from_file, get_location
from textx.exceptions import TextXSemanticError
from src.normalization import sort_for_profile

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
    """text as a DSL STRING double quotes inside are changed to single quotes"""
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
