"""
ResumeLens console program: reads a résumé and runs the four stages.
"""
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from src.extraction import extract
from src.normalization import normalize, unrecognized
from src.recognition import classify
from src.profile_dsl import to_dsl, validate, to_html


def run(text):
    """runs the four stages on a résumé text and returns what each one produced"""
    result = {}
    result["data"] = extract(text)                                    # Stage 1
    result["tokens"] = normalize(result["data"]["skills"])            # Stage 2
    result["unrecognized"] = unrecognized(result["data"]["skills"])
    result["classification"] = classify(result["tokens"])            # Stage 3
    result["dsl"] = to_dsl(result["data"], result["tokens"], result["classification"])  # Stage 4
    result["model"] = None
    result["html"] = None
    result["error"] = None
    try:
        result["model"] = validate(result["dsl"])
        result["html"] = to_html(result["model"])
    except (TextXSyntaxError, TextXSemanticError) as error:
        result["error"] = str(error)
    return result
