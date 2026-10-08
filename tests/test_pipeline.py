# Full pipeline tests (docs/08-test-cases.md, section 6)
import os
from main import run, run_file

FS = "FULL_STACK_DEVELOPER"
ML = "MACHINE_LEARNING_ENGINEER"
DO = "DEVOPS_ENGINEER"
DE = "DATA_ENGINEER"


def resume(name):
    return open(os.path.join("data", "resumes", name + ".txt"), encoding="utf-8").read()


def accepted(result):
    return [p for p, answer in result["classification"].items() if answer == "ACCEPTED"]



def test_p1_wednesday():
    result = run(resume("wednesday_addams"))
    assert result["tokens"] == ["REACT", "NODE_JS", "POSTGRESQL", "GIT", "JAVASCRIPT"]
    assert accepted(result) == [FS]


def test_p2_mary():
    result = run(resume("mary_jane_watson"))
    assert sorted(result["tokens"]) == sorted(["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"])
    assert accepted(result) == [ML]


def test_p9_every_sample_gives_a_valid_profile_and_html():
    for name in os.listdir(os.path.join("data", "resumes")):
        result = run_file(os.path.join("data", "resumes", name))
        assert result["error"] is None
        assert os.path.exists(result["html_path"])


def test_p10_missing_file():
    try:
        run_file("data/resumes/does_not_exist.txt")
        assert False
    except FileNotFoundError:
        assert True
