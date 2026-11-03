# Lab 6 - Code and Branch Coverage

Atharva Ashish Vyas | PES1UG24CS093

Starter: https://github.com/SETAPESU26/L6_L7_35_customs_duty/tree/main/lab6

The application `customs_duty.py` is unchanged from the assigned starter. This lab tests the supplied rules; it is not real customs or tax advice.

## Reproduce

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m coverage run --source=customs_duty -m pytest -q test_customs_duty.py
python -m coverage report -m
python -m coverage run --branch --source=customs_duty -m pytest -q test_customs_duty.py
python -m coverage report -m
python -m coverage run --source=customs_duty -m pytest -q CodeCoverageTest_customs_duty_application.py
python -m coverage report -m
python -m coverage run --branch --source=customs_duty -m pytest -q BranchCoverageTest_customs_duty_application.py
python -m coverage report -m
```

Explicit test filenames are required: the two handout-named deliverables do not match pytest's default `test_*.py` discovery pattern. `--source=customs_duty` measures the application, not the tests. No application lines or branches are excluded.

## Measurements

| Stage | Passing tests | Application lines | Application branches |
|---|---:|---:|---:|
| Starter tests | 2 | 13/36 (36.11%) | 7/28 (25.00%) |
| Code coverage suite | 16 | 36/36 (100%) | 27/28 (96.43%, separate diagnostic run) |
| Branch coverage suite | 39 | 36/36 (100%) | 28/28 (100%) |

When branch measurement is enabled, coverage.py's `Cover` column combines statements and branches. The exact separate percentages are recorded in the JSON reports. The starter's combined result is 31.25%; the line-suite diagnostic combined result is 98.44%.

## Deliverables

- `CodeCoverageTest_customs_duty_application.py`: stage 1, every executable statement.
- `BranchCoverageTest_customs_duty_application.py`: stage 2, both outcomes of all decisions and additional boundary cases.
- `screenshots/code_coverage.png`, `screenshots/branch_coverage.png`: screenshots of the recorded terminal output, rendered in a browser. These are not native console-window screenshots. Only successful final measurements are shown.
- `reports/`: initial, final, and diagnostic text and JSON evidence.
- Two commits: code coverage tests/evidence, then branch coverage tests/evidence.

## Analysis

The starter does not exercise electronics/clothing rates, prohibited items, negative values, paid imports, or clearance decisions. Stage 1 checks each rate, errors, gift exemptions, the minimum-duty adjustment, and all three clearance results. It achieves full statement coverage but misses the false edge of `elif value <= 1000`: its paid imports are gifts. Stage 2 adds ordinary non-gift imports above 1000, closing that missing branch.

The branch suite also checks 999/1000/1001, 4999/5000/5001, minimum duty below/at/above 50, and clearance below/at/above 20000 and 100000. It covers both prohibited categories, both FTA and non-FTA rates, gift and non-gift negative values, documents present/absent, and prohibited-category precedence over the high-value check. Expected amounts are asserted, including approximate comparisons for floating-point totals.

Line coverage asks whether a statement executed. Branch coverage asks whether each decision outcome occurred; 100% lines can still miss a branch, as stage 1 demonstrates. Path coverage considers full combinations of decisions; function coverage considers whether functions were called. All three functions are exercised here, but 100% measured branches does not prove all possible paths or inputs correct. The starter permits duty-free exemptions before checking prohibited categories in `total_duty`; tests preserve this assigned behavior rather than changing the application.
