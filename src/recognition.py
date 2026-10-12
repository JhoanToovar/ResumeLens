"""
Stage 3: recognition with finite automata (see docs/06-automata.md).
One DFA per profile, built from the profile table.
"""
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from src.profiles import PROFILES
from src.normalization import sort_for_profile


def automaton_rows(profile):
    """transitions (state, tokens, next state) and final states of a profile."""
    groups = PROFILES[profile]
    k = len(groups)
    rows = []
    for i in range(k + 1):
        # from q_i we can read a token of group j if every group between them is optional

        for j in range(i + 1, k + 1):
            rows.append(("q" + str(i), groups[j - 1][1], "q" + str(j)))
            if groups[j - 1][2] != "optional":
                break
            
        # a group with more than one token gets a loop on its own state
        if i > 0 and len(groups[i - 1][1]) > 1:
            rows.append(("q" + str(i), groups[i - 1][1], "q" + str(i)))

    finals = []
    for i in range(1, k + 1):
        rest_optional = True
        for group_name, tokens, rule in groups[i:]:
            if rule != "optional":
                rest_optional = False
        if rest_optional:
            finals.append("q" + str(i))
    return rows, finals


def build_automaton(profile):
    dfa = DeterministicFiniteAutomaton()
    dfa.add_start_state("q0")
    rows, finals = automaton_rows(profile)
    for state, tokens, next_state in rows:
        for token in tokens:
            dfa.add_transition(state, token, next_state)
    for state in finals:
        dfa.add_final_state(state)
    return dfa


AUTOMATA = {}
for profile in PROFILES:
    AUTOMATA[profile] = build_automaton(profile)


def recognize(sequence, profile):
    """True if the automaton of the profile accepts the sorted sequence"""
    return AUTOMATA[profile].accepts(sequence)


def classify(tokens):
    """Stage 3: ACCEPTED or REJECTED for each of the four profiles"""
    results = {}
    for profile in PROFILES:
        sequence = sort_for_profile(tokens, profile)
        if recognize(sequence, profile):
            results[profile] = "ACCEPTED"
        else:
            results[profile] = "REJECTED"
    return results
