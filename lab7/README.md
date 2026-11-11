# Lab 7 - Fuzzing for Input Validation Bugs

Atharva Ashish Vyas | PES1UG24CS093

Fuzz testing of the customs duty application from Lab 6 using the [Hypothesis](https://hypothesis.readthedocs.io/) property-based testing library. This lab tests the supplied rules; it is not real customs or tax advice.

## Files

| File | Description |
|------|-------------|
| `processor.py` | The customs duty application (`duty_rate`, `total_duty`, `clearance_channel`) with the bugs found by fuzzing fixed, plus a small demo `main()` |
| `test_processor.py` | Hypothesis fuzz tests for all three functions |

The submitted PDF contains the four required screenshots and both source files.

## Reproduce

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py -v
```

If `pytest` is not recognised, use `python -m pytest` as above.

## Approach

The property tested is: for any input, each function either returns a sensible result or raises `ValueError`. Any other exception (`TypeError`, `OverflowError`, ...) or a silently wrong result (`nan`, a prohibited item let through, a wrong clearance channel) counts as a bug.

`test_processor.py` contains 16 tests in three groups:

- **No-crash fuzz tests (3):** one per function, fed arbitrary values: `None`, text, integers (including huge ones), floats (including `nan` and `inf`), booleans, bytes and lists.
- **Correctness properties (8):** results are known rates, finite and non-negative, zero or at least the minimum duty, small imports and gifts are duty-free, clearance results are one of `refuse` / `inspect` / `green`, high values are inspected and low values are green.
- **Security-style properties (5):** prohibited items never get a rate, never pass `total_duty`, and are always refused at clearance (in any letter case); `nan`, `inf`, negative and huge numbers are rejected; category and origin matching is case-insensitive.

## Bugs found in the original code

| # | Bug | Example |
|---|-----|---------|
| 1 | Crashes on wrong types | `duty_rate(['x'], 'US')` raises `TypeError`; `total_duty('electronics', None, 'US', False)` raises `TypeError` |
| 2 | Crash on huge integers | `total_duty('electronics', 10**400, 'US', False)` raises `OverflowError` |
| 3 | `nan` accepted | `total_duty` returns `nan`; `clearance_channel` returns `'green'` |
| 4 | Negative values cleared | `clearance_channel(-5, 'books', True)` returns `'green'` |
| 5 | Prohibited-item check is case-sensitive | `'WEAPONS'` gets a 15% rate; `'Narcotics'` is cleared `'green'` |
| 6 | Prohibited items bypass `total_duty` | `total_duty('weapons', 500, 'US', False)` returns `0` because the duty-free exemption returns before the prohibited check |
| 7 | Category and origin are case-sensitive | `'Electronics'` gets the default 15% instead of 20%; `'fta'` is not treated as FTA |
| 8 | Truthy flags accepted | `total_duty('books', 5000, 'US', 'no')` treats `'no'` as a gift |

## Fix

Small helper validators (`_clean_category`, `_clean_origin`, `_clean_value`, `_clean_flag`) check every argument before it is used:

- category and origin must be strings; they are stripped and compared case-insensitively, and an empty category is rejected;
- value must be a real number (not a bool), finite, non-negative and small enough to convert to a float;
- `is_gift` and `has_documents` must be real booleans;
- prohibited categories are rejected before any exemption can return `0`;
- every invalid input raises `ValueError` with a clear message.

Valid inputs behave exactly as in the original code. One deliberate change from Lab 6: `total_duty` now rejects prohibited items even when the value is under the duty-free thresholds. Lab 6 preserved the old behaviour only to test the assigned code as supplied; fuzzing shows it is a real hole.

## Results

| Run | Passed | Failed |
|-----|-------:|-------:|
| `test_processor.py` against the original `processor.py` | 8 | 8 |
| `test_processor.py` against the fixed `processor.py` | 16 | 0 |

`python processor.py` runs a short demo: against the original code it shows crashes and wrong results; against the fixed code the same inputs print `REJECTED (ValueError: ...)` and valid inputs still return correct results.

## Notes

- A passing fuzz run does not prove the code correct; Hypothesis explores many inputs but not all of them.
- The `.hypothesis/` and `.pytest_cache/` folders are created by the test run and are not committed.
