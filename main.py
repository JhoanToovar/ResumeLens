"""
ResumeLens console program: reads a résumé and runs the four stages.
"""
import os
import glob
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from src.extraction import extract, save_extraction
from src.normalization import normalize, unrecognized, sort_for_profile
from src.recognition import classify
from src.profile_dsl import to_dsl, validate, to_html

RESUMES_DIR = os.path.join("data", "resumes")
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


def show(result):
    data = result["data"]
    print("\n--- Stage 1: extraction (regex) ---")
    print("Name:", data["name"])
    print("Email:", data["email"], "| Phone:", data["phone"], "| URLs:", data["urls"])
    print("Education:", [e["line"] for e in data["education"]])
    print("Jobs:", [j["role"] + " at " + j["company"] for j in data["jobs"]])
    print("Experience:", [str(e["years"]) + " years " + e["description"] for e in data["experience"]])
    print("Skills as written:", ", ".join(data["skills"]))

    print("\n--- Stage 2: normalization (transducers) ---")
    print("Tokens:", ", ".join(result["tokens"]))
    if result["unrecognized"]:
        print("Not recognized:", ", ".join(result["unrecognized"]))

    print("\n--- Stage 3: recognition (automata) ---")
    for profile, answer in result["classification"].items():
        sequence = sort_for_profile(result["tokens"], profile)
        print(profile.ljust(26), answer.ljust(9), " ".join(sequence))

    print("\n--- Stage 4: candidate profile (textX DSL) ---")
    print(result["dsl"])
    if result["error"]:
        print("\nINVALID PROFILE:", result["error"])
    else:
        print("\nValid profile. HTML written to", result["html_path"])


def main():
    print("ResumeLens - formal language-based résumé screening")
    while True:
        files = sorted(glob.glob(os.path.join(RESUMES_DIR, "*.txt")))
        print("\nSample résumés:")
        for i, path in enumerate(files, start=1):
            print(" ", i, os.path.basename(path))
        option = input("\nNumber of a sample, path of a .txt file, or q to quit: ").strip()
        if option.lower() == "q":
            break
        if option.isdigit() and 1 <= int(option) <= len(files):
            path = files[int(option) - 1]
        else:
            path = option
        try:
            show(run_file(path))
        except FileNotFoundError:
            print("File not found:", path)
        except UnicodeDecodeError:
            print("The file is not a text file:", path)


if __name__ == "__main__":
    main()
