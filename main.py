"""
ResumeLens console program: reads a résumé and runs the four stages.
"""
import os
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from src.extraction import extract, save_extraction
from src.normalization import normalize, unrecognized
from src.recognition import classify
from src.profile_dsl import to_dsl, validate, to_html

OUTPUT_DIR = "output"


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


def run_file(path):
    """runs the pipeline on a file and writes the JSON and HTML outputs"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    result = run(text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    save_extraction(result["data"], os.path.join(OUTPUT_DIR, base + ".json"))
    result["html_path"] = None
    if result["html"]:
        result["html_path"] = os.path.join(OUTPUT_DIR, base + ".html")
        with open(result["html_path"], "w", encoding="utf-8") as f:
            f.write(result["html"])
    return result
