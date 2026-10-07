"""
candidate profile DSL with textX (see docs/07-grammar.md)
"""
import os
from textx import metamodel_from_file

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "resumelens.tx")
mm = metamodel_from_file(GRAMMAR_FILE)



def validate(dsl_text):
    """returns the textX model; raises TextXSyntaxError or TextXSemanticError if it is not valid"""
    return mm.model_from_str(dsl_text)
