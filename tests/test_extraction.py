# Stage 1 tests (docs/08-test-cases.md, section 2)
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


def test_e3_education_and_job():
    data = extract(R3)
    assert data["education"][0]["degree"] == "B.Sc."
    assert data["education"][0]["year"] == "2022"
    assert data["jobs"][0] == {"role": "Backend Developer", "company": "Umbrella Corporation",
                               "start": "2022", "end": "present"}


def test_e4_years_of_experience():
    assert extract(R1)["experience"] == [{"years": 3, "description": "developing web applications"}]


def test_frameworks_databases_and_tools():
    found = extract(R1)["skills_by_type"]
    assert found["frameworks"] == ["React.js", "NodeJS"]
    assert found["databases"] == ["Postgres"]
    assert found["tools"] == ["Git"]


def test_e7_non_technical_skills():
    assert extract(R7)["skills"] == []


def test_e8_no_skills_section():
    assert extract(R8)["skills"] == []


def test_e1_skills_from_assignment():
    assert extract(R1)["skills"] == ["React.js", "NodeJS", "Postgres", "Git", "JS"]


def test_e5_short_names_inside_longer_ones():
    skills = extract("Skills: React JS, My SQL, SQL Server, T-SQL")["skills"]
    assert sorted(skills) == sorted(["React JS", "My SQL", "SQL Server", "T-SQL"])
    assert "JS" not in skills
    assert "SQL" not in skills


def test_e6_java_and_javascript():
    assert sorted(extract("Skills: Java, JavaScript")["skills"]) == ["Java", "JavaScript"]
