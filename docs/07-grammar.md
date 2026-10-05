# Stage 4: Candidate Profile Language (DSL)

After Stages 1 to 3, ResumeLens has the candidate's data, the canonical skill tokens and the profiles that accepted them. Stage 4 writes all of that in a small language of our own, checks it with a context-free grammar implemented in textX and, if it is valid, turns it into an HTML page.

The grammar does not extract or classify anything. It only defines how a candidate profile must be written.

## 1. What a candidate profile looks like

The résumé from the assignment, after the pipeline:

```
candidate "Wednesday Addams" {
    experience {
        years 3
        description "developing web applications"
    }
    skills { JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT }
    accepted {
        profile FULL_STACK_DEVELOPER : JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
    }
}
```

A fuller one, with every kind of block:

```
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
}
```

Each line inside `accepted` names one accepted profile and the tokens that matched it. If no profile accepted the résumé, the block is written empty: `accepted { }`.

## 2. Grammar in EBNF

Notation: `=` defines a rule, `,` is concatenation, `|` is choice, `[ ]` is optional, `{ }` is zero or more repetitions, and quoted text is a literal.

```ebnf
candidate      = "candidate", string, "{",
                     [ contact ],
                     { education },
                     { experience },
                     skills,
                     accepted,
                 "}" ;

contact        = "contact", "{",
                     [ "email", email ],
                     [ "phone", phone ],
                     { "url", url },
                 "}" ;

education      = "education", "{",
                     "degree", string,
                     [ "institution", string ],
                     [ "year", year ],
                 "}" ;

experience     = "experience", "{",
                     [ "role", string ],
                     [ "company", string ],
                     [ "years", integer ],
                     [ "period", year, "-", end year ],
                     [ "description", string ],
                 "}" ;

skills         = "skills", "{", [ token, { ",", token } ], "}" ;

accepted       = "accepted", "{", { profile result }, "}" ;

profile result = "profile", profile name, ":", token, { ",", token } ;

profile name   = "FULL_STACK_DEVELOPER" | "MACHINE_LEARNING_ENGINEER"
               | "DEVOPS_ENGINEER" | "DATA_ENGINEER" ;

end year       = year | "present" ;

(* lexical rules *)
token          = upper, { upper | digit | "_" } ;
year           = ( "19" | "20" ), digit, digit ;
integer        = digit, { digit } ;
string         = '"', { any character except '"' }, '"' ;
email          = user part, "@", domain ;       (* regex in section 4 *)
phone          = [ "+" ], digit, { digit | " " | "(" | ")" | "-" }, digit ;
url            = [ "http://" | "https://" ], domain, { "/", path part } ;
```

## 3. Terminals and non-terminals

| Non-terminals | Meaning |
|---|---|
| `candidate` | start symbol, the whole profile |
| `contact`, `education`, `experience`, `skills`, `accepted` | the blocks of the profile |
| `profile result` | one accepted profile and its matched tokens |
| `profile name`, `end year` | small choices used inside blocks |

| Terminals | Kind |
|---|---|
| `candidate`, `contact`, `email`, `phone`, `url`, `education`, `degree`, `institution`, `year`, `experience`, `role`, `company`, `years`, `period`, `description`, `skills`, `accepted`, `profile`, `present` | keywords |
| `{`, `}`, `,`, `:`, `-` | punctuation |
| `FULL_STACK_DEVELOPER`, `MACHINE_LEARNING_ENGINEER`, `DEVOPS_ENGINEER`, `DATA_ENGINEER` | profile names |
| `token`, `year`, `integer`, `string`, `email`, `phone`, `url` | lexical terminals, defined by a regular expression |

## 4. Implementation in textX

File `src/resumelens.tx`. It is the same grammar written in textX syntax: `*=` is zero or more, `+=` is one or more, `?` is optional and `[',']` means "separated by commas", as in the textX sessions and Follow-up 4.

```
Candidate:
    'candidate' name=STRING '{'
        contact=Contact?
        education*=Education
        experience*=Experience
        skills=Skills
        accepted=Accepted
    '}'
;

Contact:
    'contact' '{'
        ('email' email=Email)?
        ('phone' phone=Phone)?
        ('url' urls=Url)*
    '}'
;

Education:
    'education' '{'
        'degree' degree=STRING
        ('institution' institution=STRING)?
        ('year' year=Year)?
    '}'
;

Experience:
    'experience' '{'
        ('role' role=STRING)?
        ('company' company=STRING)?
        ('years' years=INT)?
        ('period' start=Year '-' end=EndYear)?
        ('description' description=STRING)?
    '}'
;

Skills:
    'skills' '{' tokens*=Token[','] '}'
;

Accepted:
    'accepted' '{' profiles*=ProfileResult '}'
;

ProfileResult:
    'profile' profile=ProfileName ':' matched+=Token[',']
;

ProfileName:
    'FULL_STACK_DEVELOPER' | 'MACHINE_LEARNING_ENGINEER' | 'DEVOPS_ENGINEER' | 'DATA_ENGINEER'
;

Token: /[A-Z][A-Z0-9_]*/;
Email: /[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}/;
Phone: /\+?\d[\d ()-]{6,18}\d/;
Url: /(https?:\/\/)?(www\.)?[\w-]+(\.[\w-]+)+(\/[\w.-]+)*/;
Year: /(19|20)\d\d/;
EndYear: Year | 'present';
```

The metamodel is built with `metamodel_from_file('resumelens.tx')` and a profile is read with `model_from_str(text)`. The result is a Python object: `model.name`, `model.skills.tokens`, `model.accepted.profiles[0].profile`, and so on. The HTML page is generated from that object.

## 5. Structure of the language

- **Fixed order of blocks.** Contact, education, experience, skills and accepted always appear in that order. A profile with `skills` before `experience` is rejected.
- **Optional and repeated blocks.** `contact` is optional. `education` and `experience` can appear zero or more times, one block per degree or job. `skills` and `accepted` are always present, even if empty, so a reader always knows the classification was done.
- **Nesting.** The candidate contains blocks and each block contains fields. Braces mark where each block starts and ends.
- **Lists.** Skills and matched tokens are comma-separated lists. A matched-token list needs at least one token, since a profile cannot be accepted with nothing.
- **Same lexical rule as Stage 2.** `Token` is the naming rule from `02-profiles-and-vocabulary.md` (uppercase, digits, underscore). Any token produced by the transducers is a valid DSL token, and a lowercase or misspelled one is a lexical error.

The nesting here has a fixed depth, so this particular language could in theory be described by a very large regular expression. We use a context-free grammar because it states the structure directly (a candidate is made of blocks, a block is made of fields) and because textX builds the object model from it, which is what Stage 4 needs to produce the HTML.

## 6. Validation

A profile is valid only if textX parses it. textX checks the lexical rules (each terminal matches its regex) and the syntactic rules (the order and nesting of the grammar) at once, and raises `TextXSyntaxError` with the line and column of the first error.

| Invalid input | Rule broken | textX message (shortened) |
|---|---|---|
| `email leon.kennedy@` | lexical: not an `Email` | `Expected Email` |
| `skills { JAVASCRIPT, react }` | lexical: `react` is not a `Token` | `Expected Token` |
| `year 22` | lexical: not a `Year` | `Expected Year` |
| `profile DATA_SCIENTIST : PYTHON` | lexical: not a `ProfileName` | `Expected 'FULL_STACK_DEVELOPER' or ...` |
| `skills` block written before `experience` | syntactic: wrong order | `Expected 'accepted'` |
| last `}` missing | syntactic: block not closed | `Expected '}'` |

There is one more check that a grammar cannot express: every token listed under an accepted profile must also appear in `skills`. It is done with an object processor registered on `Candidate`, the same mechanism as Follow-up 4, and it raises `TextXSemanticError`:

```
profile FULL_STACK_DEVELOPER : TYPESCRIPT, ...     (TYPESCRIPT not in skills)
-> TYPESCRIPT is used in FULL_STACK_DEVELOPER but is not listed in skills
```

All the examples in sections 1 and 6 were run against the grammar in textX and give the results shown.

## 7. Visualization

When the profile is valid, `to_html(model)` builds one HTML page with:

- the name and the contact data, if present
- one entry per education block and per experience block
- the skills as a list of tags
- one section per accepted profile with its matched tokens, or the text "No profile accepted"

The page is saved in `output/` with the candidate's name as file name and can be opened in any browser.
