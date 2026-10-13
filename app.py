"""
Run it with:  streamlit run app.py
"""
import os
import glob
import streamlit as st
from main import run, RESUMES_DIR
from src.normalization import sort_for_profile
from src.profiles import PROFILE_TITLES

OWN_TEXT = "(write or paste my own)"


def show(value):
    """text to show for a value that may be missing"""
    if value is None or value == "" or value == []:
        return "not found"
    return value

st.set_page_config(page_title="ResumeLens", layout="wide")
st.title("ResumeLens")
st.caption("Formal language-based résumé screening: regular expressions → transducers → automata → textX DSL")

# ---------- input ----------
files = sorted(glob.glob(os.path.join(RESUMES_DIR, "*.txt")))
names = [os.path.basename(path) for path in files]
choice = st.selectbox("Sample résumé", [OWN_TEXT] + names)

sample_text = ""
if choice != OWN_TEXT:
    with open(os.path.join(RESUMES_DIR, choice), encoding="utf-8") as f:
        sample_text = f.read()
text = st.text_area("Résumé text", value=sample_text, height=220)

if st.button("Analyze", type="primary"):
    if text.strip() == "":
        st.warning("Choose a sample or write a résumé first.")
    else:
        result = run(text)
        data = result["data"]

        # ---------- Stage 1 ----------
        st.header("Stage 1: extraction (regular expressions)")
        left, right = st.columns(2)
        with left:
            st.write("**Name:**", show(data["name"]))
            st.write("**Email:**", show(data["email"]))
            st.write("**Phone:**", show(data["phone"]))
            st.write("**URLs:**", show(", ".join(data["urls"])))
        with right:
            st.write("**Education:**", show("; ".join([e["line"] for e in data["education"]])))
            st.write("**Jobs:**", show("; ".join([j["role"] + " at " + j["company"] for j in data["jobs"]])))
            st.write("**Experience:**", show("; ".join([str(e["years"]) + " years " + e["description"] for e in data["experience"]])))
        st.write("**Skills as written, by type:**")
        for skill_type, skills in data["skills_by_type"].items():
            st.write("-", skill_type + ":", ", ".join(skills) if skills else "none")

        # ---------- Stage 2 ----------
        st.header("Stage 2: normalization (finite-state transducers)")
        st.code(", ".join(result["tokens"]) if result["tokens"] else "no tokens")
        if result["unrecognized"]:
            st.warning("Not recognized: " + ", ".join(result["unrecognized"]))

        # ---------- Stage 3 ----------
        st.header("Stage 3: recognition (finite automata)")
        rows = []
        for profile, answer in result["classification"].items():
            rows.append({
                "Profile": PROFILE_TITLES[profile],
                "Result": answer,
                "Sorted sequence read by the automaton": " ".join(sort_for_profile(result["tokens"], profile)),
            })
        st.table(rows)

        # ---------- Stage 4 ----------
        st.header("Stage 4: candidate profile (textX DSL)")
        st.code(result["dsl"])
        if result["error"]:
            st.error("Invalid profile: " + result["error"])
        else:
            st.success("Valid profile")
            st.iframe(result["html"], height=650)
