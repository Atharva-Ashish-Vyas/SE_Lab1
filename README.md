# Software Engineering Lab Portfolio

**Student:** Atharva Ashish Vyas  
**SRN:** PES1UG24CS093  
**Course:** Software Engineering

This repository contains my Software Engineering laboratory submissions. Each lab is kept in its own folder with the code, reports, test evidence, and documentation required for that exercise.

## Labs

| Lab | Topic | Main deliverables |
|---|---|---|
| [Lab 1](./Lab1_PES1UG24CS093_B.pdf) | Requirements Engineering and UML Use-Case Modelling | Requirements table, UML use-case diagram, and use-case specification for a telemedicine portal |
| [Lab 3](./Lab3) | Software Architecture | Component diagram and design justification |
| [Lab 4](./Lab-4) | Prompt Engineering and Game Development | Source code, report, prompt record, evidence, and video material |
| [Lab 5](./lab5) | Static Code Analysis | Cleaned parcel tracker, Pylint, Bandit, and Flake8 reports, issue analysis, and reflection |
| [Lab 6](./lab6) | Code and Branch Coverage | Customs-duty tests, coverage reports, and final coverage evidence |
| [Lab 7](./lab7) | Fuzz Testing | Fuzz-testing report, processor implementation, and automated tests |

## Repository structure

```text
SE_Lab1/
├── Lab1_PES1UG24CS093_B.pdf
├── Lab3/
├── Lab-4/
├── lab5/
├── lab6/
└── lab7/
```

## Highlights

### Lab 5 - Static Code Analysis

The parcel-tracker application was improved using Pylint, Bandit, and Flake8. The final version achieves:

- Pylint score: **10.00/10**
- Flake8: **no findings**
- Bandit: **no active findings**

The work is documented in [lab5](./lab5), including before-and-after reports, issue fixes, and reflection answers.

### Lab 6 - Code and Branch Coverage

The customs-duty calculator is tested using separate suites for code coverage and branch coverage:

- Statement coverage: **100% (36/36 statements)**
- Branch coverage: **100% (28/28 branches)**
- Code coverage suite: **16 passing tests**
- Branch coverage suite: **39 passing tests**

Commands, reports, screenshots, and test design notes are available in [lab6](./lab6).

## Running Python-based labs

Labs that include Python code can generally be run from their own folder.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Refer to the README or submission documentation inside the relevant lab folder for exact commands and dependencies.

## Notes

- Each lab is an independent academic exercise.
- Reports and screenshots are included as evidence for the applicable lab requirements.
- Source repositories assigned for individual exercises are referenced within the corresponding lab documentation.
