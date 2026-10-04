# Literature Review

This review covers the four formal models used by ResumeLens and the problem they are applied to: reading résumés written in free text. For each topic we note what we took from the source and how it changes our design.

## 1. Information extraction from résumés

Résumé parsing is an old problem. Yu, Guan and Zhou (2005) split it into two passes: first the résumé is cut into blocks (personal data, education, experience) and then each block is processed with its own model. Çelik and Elçi (2013) used an ontology of skills and job concepts to decide what each extracted phrase means. Both papers show the same difficulty that the assignment mentions: the same skill is written in many ways, and a parser that only looks for one spelling misses most candidates.

Most recent systems use statistical models or LLMs. Rule-based extraction is still common in industry because rules can be read, tested and fixed one at a time (Chiticariu, Li and Reiss, 2013). That fits this project. We need every decision to be explainable with a formal model, not with a trained weight.

What we take: a two-step idea (find candidate strings first, decide what they mean later). This is exactly the split between Stage 1 (regex) and Stage 2 (FST).

## 2. Regular expressions

Regular expressions describe regular languages, the same class recognized by finite automata (Hopcroft, Motwani and Ullman, 2006, ch. 3). Python's `re` module adds features that go beyond that class, like backreferences and lookarounds. We used both in Follow-up 1.

What we take: each extraction pattern will be written so it can be explained as a language over characters. When we use a lookaround, we use it only for word boundaries, such as `(?<!\w)` to avoid catching "Java" inside "JavaScript", and we say so in the documentation.

## 3. Finite-state transducers for normalization

A finite-state transducer reads an input string and writes an output string while it moves between states. Mohri (1997) shows how transducers are used in language processing for rewriting, for example turning several spellings of a word into one form. Beesley and Karttunen (2003) use the same idea for morphology, where many surface forms map to one lemma.

Skill taxonomies such as ESCO (European Commission) and job-posting datasets such as SkillSpan (Zhang et al., 2022) keep a preferred label for each skill plus a list of alternative labels. That is the same structure we need: one canonical token and a set of surface variants.

What we take: one canonical token per qualification (for example `NODE_JS`) with an explicit list of variants (`NodeJS`, `Node.js`, `Node`). The list of canonical tokens is the output alphabet Γ of our transducers.

## 4. Finite automata for pattern recognition

DFAs, NFAs and ε-NFAs recognize the same languages and can be converted into each other (Hopcroft, Motwani and Ullman, 2006, ch. 2). An NFA is often easier to draw for a pattern like "at least one frontend framework, then at least one backend technology". A DFA is easier to run and to test. Pyformlang (Romero, 2021) implements all three types, including conversion and minimization, plus transducers, so one library covers Stages 2 and 3. We already used it in Follow-ups 2 and 3.

What we take: each profile pattern will be a regular language over canonical tokens. Since the tokens are sorted in a fixed order per profile before reaching the automaton, the pattern becomes a sequence of groups, and the automaton stays small.

## 5. Context-free grammars and DSLs

A domain-specific language is a small language made for one problem (Fowler, 2010). textX builds a parser and a meta-model from a single grammar written in an EBNF-like notation, and the parsed model comes back as Python objects (Dejanović et al., 2017). We used it in Follow-up 4. This lets the candidate profile be validated by the parser: if the text does not follow the grammar, textX rejects it with a syntax error.

What we take: the candidate profile is written as a DSL document. Repeated sections (experience, education, skills) are modeled with the `*=` and `+=` repetition operators, and the visualization is produced from the parsed model, never from the raw text.

## 6. Limits of automated screening

Raghavan, Barocas, Kleinberg and Levy (2020) reviewed commercial hiring tools and found that most do not explain how they score candidates and can reproduce bias present in their data. The assignment says ResumeLens must not rank candidates or make hiring decisions.

What we take: ResumeLens only reports whether the qualifications written in the résumé match a pattern. It does not score, rank or infer skills that are not written. Every result can be traced back to the regex that found a string, the transducer that normalized it and the automaton that accepted it.

## Design decisions taken from this review

| Decision | Source |
|---|---|
| Extraction and normalization are separate stages | Yu et al. (2005), Chiticariu et al. (2013) |
| One canonical token per skill with a list of variants | ESCO, Zhang et al. (2022), Mohri (1997) |
| Profiles are regular languages over canonical tokens, sorted per profile | Hopcroft et al. (2006) |
| Pyformlang for transducers and automata | Romero (2021) |
| Candidate profile as a textX DSL, validated by its parser | Fowler (2010), Dejanović et al. (2017) |
| Only explicit qualifications count, no ranking | Raghavan et al. (2020), assignment statement |

## References

- Beesley, K. R., and Karttunen, L. (2003). *Finite State Morphology*. CSLI Publications.
- Çelik, D., and Elçi, A. (2013). An ontology-based information extraction approach for résumés. In *Pervasive Computing and the Networked World*, LNCS 7719. Springer. https://doi.org/10.1007/978-3-642-37015-1_14
- Chiticariu, L., Li, Y., and Reiss, F. R. (2013). Rule-based information extraction is dead! Long live rule-based information extraction systems! In *Proceedings of EMNLP 2013*, pp. 827-832. https://aclanthology.org/D13-1079/
- Dejanović, I., Vaderna, R., Milosavljević, G., and Vuković, Ž. (2017). TextX: A Python tool for Domain-Specific Languages implementation. *Knowledge-Based Systems*, 115, 1-4.
- European Commission. ESCO: European Skills, Competences, Qualifications and Occupations. https://esco.ec.europa.eu/
- Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley.
- Hopcroft, J. E., Motwani, R., and Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.
- Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational Linguistics*, 23(2), 269-311. https://aclanthology.org/J97-2003/
- Raghavan, M., Barocas, S., Kleinberg, J., and Levy, K. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. In *Proceedings of FAT\* 2020*, pp. 469-481. https://doi.org/10.1145/3351095.3372828
- Romero, J. (2021). Pyformlang: An educational library for formal language manipulation. In *Proceedings of SIGCSE 2021*. https://doi.org/10.1145/3408877.3432464
- Yu, K., Guan, G., and Zhou, M. (2005). Resume information extraction with cascaded hybrid model. In *Proceedings of ACL 2005*, pp. 499-506.
- Zhang, M., Jensen, K. N., Sonniks, S., and Plank, B. (2022). SkillSpan: Hard and soft skill extraction from English job postings. In *Proceedings of NAACL 2022*. https://aclanthology.org/2022.naacl-main.366/
