# Stage 4 tests (docs/08-test-cases.md, section 5)
import pytest
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from src.profile_dsl import validate, to_html, to_dsl

WEDNESDAY = '''
candidate "Wednesday Addams" {
    experience {
        years 3
        description "developing web applications"
    }
    skills { JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT }
    accepted {
        profile FULL_STACK_DEVELOPER : JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
    }
}'''

LEON = '''
candidate "Leon Kennedy" {
    contact {
        email leon.kennedy@rpd.example.com
        phone +57 300 123 4567
        url linkedin.com/in/leon-kennedy
        url https://github.com/lkennedy
    }
    education {
        degree "B.Sc. in Systems Engineering"
        institution "Universidad Icesi"
        year 2022
    }
    experience {
        role "Backend Developer"
        company "Umbrella Corporation"
        period 2022 - present
    }
    skills { TYPESCRIPT, REACT, NODE_JS, MYSQL, GIT }
    accepted {
        profile FULL_STACK_DEVELOPER : TYPESCRIPT, REACT, NODE_JS, MYSQL, GIT
    }
}'''



def test_d1_minimal_profile():
    assert validate(WEDNESDAY).name == "Wednesday Addams"


def test_d2_profile_with_every_block():
    model = validate(LEON)
    assert len(model.contact.urls) == 2
    assert model.education[0].year == "2022"
    assert model.experience[0].end == "present"


def test_d3_no_accepted_profile():
    text = WEDNESDAY.replace(
        "profile FULL_STACK_DEVELOPER : JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT", "")
    assert validate(text).accepted.profiles == []


def test_d4_bad_email():
    with pytest.raises(TextXSyntaxError):
        validate(LEON.replace("leon.kennedy@rpd.example.com", "leon.kennedy@"))


def test_d5_lowercase_token():
    with pytest.raises(TextXSyntaxError):
        validate(WEDNESDAY.replace("skills { JAVASCRIPT, REACT", "skills { JAVASCRIPT, react"))


def test_d6_unknown_profile():
    with pytest.raises(TextXSyntaxError):
        validate(WEDNESDAY.replace("FULL_STACK_DEVELOPER", "DATA_SCIENTIST"))


def test_d7_wrong_order():
    experience = '''    experience {
        years 3
        description "developing web applications"
    }
'''
    skills = "    skills { JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT }\n"
    text = WEDNESDAY.replace(experience + skills, skills + experience)
    with pytest.raises(TextXSyntaxError):
        validate(text)


def test_d8_block_not_closed():
    with pytest.raises(TextXSyntaxError):
        validate(WEDNESDAY.rstrip()[:-1])


def test_d9_matched_token_not_in_skills():
    text = WEDNESDAY.replace("profile FULL_STACK_DEVELOPER : JAVASCRIPT", "profile FULL_STACK_DEVELOPER : TYPESCRIPT")
    with pytest.raises(TextXSemanticError):
        validate(text)


def test_to_dsl_writes_a_valid_profile():
    data = {"name": "Wednesday Addams", "email": None, "phone": None, "urls": [],
            "education": [], "jobs": [],
            "experience": [{"years": 3, "description": "developing web applications"}]}
    tokens = ["REACT", "NODE_JS", "POSTGRESQL", "GIT", "JAVASCRIPT"]
    results = {"FULL_STACK_DEVELOPER": "ACCEPTED", "MACHINE_LEARNING_ENGINEER": "REJECTED",
               "DEVOPS_ENGINEER": "REJECTED", "DATA_ENGINEER": "REJECTED"}
    model = validate(to_dsl(data, tokens, results))
    assert model.accepted.profiles[0].matched == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]


def test_d10_html_output():
    page = to_html(validate(WEDNESDAY))
    assert "Wednesday Addams" in page
    for token in ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]:
        assert token in page
    assert "FULL_STACK_DEVELOPER" in page
