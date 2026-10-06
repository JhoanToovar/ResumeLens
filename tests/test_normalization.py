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
