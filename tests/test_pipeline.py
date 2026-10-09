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


def test_p3_leon():
    result = run(resume("leon_kennedy"))
    assert len(result["tokens"]) == 15
    assert "HTML" not in result["data"]["skills"]
    assert accepted(result) == [FS]


def test_p4_chris():
    result = run(resume("chris_redfield"))
    assert len(result["tokens"]) == 14
    assert accepted(result) == [DO]


def test_p5_catherine():
    result = run(resume("catherine_halsey"))
    assert len(result["tokens"]) == 8
    assert accepted(result) == [DE]


def test_p6_ada_two_profiles():
    result = run(resume("ada_wong"))
    assert len(result["tokens"]) == 9
    assert result["tokens"].count("JAVASCRIPT") == 1
    assert accepted(result) == [ML, DE]


def test_p7_p8_no_skills():
    for name in ["jill_valentine", "avery_johnson"]:
        result = run(resume(name))
        assert result["tokens"] == []
        assert accepted(result) == []
        assert result["model"].accepted.profiles == []
