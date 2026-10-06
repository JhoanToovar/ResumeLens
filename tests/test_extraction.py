# Stage 1 tests 
from src.extraction import extract

R1 = open("data/resumes/wednesday_addams.txt", encoding="utf-8").read()
R3 = open("data/resumes/leon_kennedy.txt", encoding="utf-8").read()
R7 = open("data/resumes/jill_valentine.txt", encoding="utf-8").read()
R8 = open("data/resumes/avery_johnson.txt", encoding="utf-8").read()


def test_e2_candidate_data():
    data = extract(R3)
    assert data["name"] == "Leon Kennedy"
    assert data["email"] == "leon.kennedy@rpd.example.com"
    assert data["phone"] == "+57 300 123 4567"
    assert data["urls"] == ["linkedin.com/in/leon-kennedy"]


def test_e9_invalid_email():
    assert extract("leon@site")["email"] is None
