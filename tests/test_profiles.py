# profiles.py tests
from src.profiles import PROFILES, PROFILE_TITLES, profile_order


def test_four_profiles():
    assert list(PROFILES) == ["FULL_STACK_DEVELOPER", "MACHINE_LEARNING_ENGINEER", "DEVOPS_ENGINEER", "DATA_ENGINEER"]
    assert list(PROFILE_TITLES) == list(PROFILES)


def test_rules_are_valid():
    for profile, groups in PROFILES.items():
        for group_name, tokens, rule in groups:
            assert rule in ["required", "at_least_one", "optional"]
            assert len(tokens) > 0


def test_every_profile_ends_with_git():
    for profile, groups in PROFILES.items():
        assert groups[-1] == ("Version control", ["GIT"], "required")


def test_profile_order_full_stack():
    order = profile_order("FULL_STACK_DEVELOPER")
    assert order[:3] == ["JAVASCRIPT", "TYPESCRIPT", "REACT"]
    assert order[-1] == "GIT"
    assert len(order) == 20
