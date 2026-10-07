# Stage 3 tests (docs/08-test-cases.md, section 4)
from src.recognition import recognize, automaton_rows, AUTOMATA

FS = "FULL_STACK_DEVELOPER"
ML = "MACHINE_LEARNING_ENGINEER"
DO = "DEVOPS_ENGINEER"
DE = "DATA_ENGINEER"



def test_a1():
    assert recognize("JAVASCRIPT REACT NODE_JS POSTGRESQL GIT".split(), FS)


def test_a2_optional_group_and_two_databases():
    assert recognize("TYPESCRIPT ANGULAR SPRING_BOOT REST_API MYSQL MONGODB GIT".split(), FS)


def test_a3_no_backend():
    assert not recognize("JAVASCRIPT REACT POSTGRESQL GIT".split(), FS)


def test_a4_assignment_example():
    assert recognize("PYTHON PANDAS TENSORFLOW POSTGRESQL GIT".split(), ML)


def test_a5_no_ml_library():
    assert not recognize("PYTHON PANDAS NUMPY SQL GIT".split(), ML)


def test_a11_ends_before_git():
    assert not recognize("JAVASCRIPT REACT NODE_JS POSTGRESQL".split(), FS)


def test_a12_all_deterministic():
    for profile, dfa in AUTOMATA.items():
        assert dfa.is_deterministic()


def test_rows_match_the_design():
    rows, finals = automaton_rows("FULL_STACK_DEVELOPER")
    assert len(rows) == 12
    assert finals == ["q6"]
