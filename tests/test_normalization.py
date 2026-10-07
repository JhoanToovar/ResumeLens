# Stage 2 tests (docs/08-test-cases.md, section 3)
from src.normalization import to_symbols, normalize, normalize_skill, unrecognized, TRANSDUCERS, VARIANTS


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


def test_n4_multi_word_variants():
    assert normalize_skill("GitLab CI/CD") == "GITLAB_CI"
    assert normalize_skill("Google Cloud Platform") == "GCP"


def test_n5_prefix_that_is_not_a_skill():
    assert normalize_skill("Spring") is None


def test_n6_unknown_skill():
    assert unrecognized(["HTML", "Reac", "Git"]) == ["HTML", "Reac"]


def test_n7_repeated_skill():
    assert normalize(["JS", "JavaScript"]) == ["JAVASCRIPT"]


def test_every_variant_gives_its_token():
    for name, table in VARIANTS.items():
        for token, variants in table.items():
            for raw in variants:
                assert normalize_skill(raw) == token


def test_transducer_sizes_match_the_design():
    sizes = {name: len(fst.states) for name, fst in TRANSDUCERS.items()}
    assert sizes == {"T_LANG": 13, "T_FW": 27, "T_DB": 18, "T_TOOL": 33, "T_OTHER": 6}


TOKENS = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]
