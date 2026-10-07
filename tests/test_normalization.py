# Stage 2 tests (docs/08-test-cases.md, section 3)
from src.normalization import to_symbols, normalize_skill, TRANSDUCERS


def test_to_symbols():
    assert to_symbols("React.js") == ["react", "js", "#"]
    assert to_symbols("GitLab CI/CD") == ["gitlab", "ci", "cd", "#"]
    assert to_symbols("Scikit-learn") == to_symbols("scikit learn")


def test_languages():
    assert normalize_skill("JS") == "JAVASCRIPT"
    assert normalize_skill("Python 3") == "PYTHON"
    assert normalize_skill("Python3") == "PYTHON"
    assert normalize_skill("PL/SQL") == "SQL"
    assert normalize_skill("Shell scripting") == "BASH"


def test_unknown_word_is_rejected():
    assert normalize_skill("Cobol") is None


def test_language_transducer_size():
    assert len(TRANSDUCERS["T_LANG"].states) == 13


def test_n1_variants_from_assignment():
    result = [normalize_skill(raw) for raw in ["JS", "React.js", "NodeJS", "Postgres"]]
    assert result == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL"]


def test_n2_different_separators():
    for raw in ["Scikit-learn", "Scikit learn", "sklearn"]:
        assert normalize_skill(raw) == "SCIKIT_LEARN"


def test_n3_case_does_not_matter():
    for raw in ["NUMPY", "numpy", "NumPy"]:
        assert normalize_skill(raw) == "NUMPY"


def test_frameworks_and_databases_sizes():
    assert len(TRANSDUCERS["T_FW"].states) == 27
    assert len(TRANSDUCERS["T_DB"].states) == 18
