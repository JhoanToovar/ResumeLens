"""
Stage 4: candidate profile DSL with textX (see docs/07-grammar.md).
"""
import os
from textx import metamodel_from_file, get_location
from textx.exceptions import TextXSemanticError

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



def validate(dsl_text):
    """returns the textX model; raises TextXSyntaxError or TextXSemanticError if it is not valid"""
    return mm.model_from_str(dsl_text)
