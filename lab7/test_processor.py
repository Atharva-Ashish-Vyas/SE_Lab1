"""Hypothesis fuzz tests for processor.py (customs duty application).

Contract being tested: for ANY input a function either returns a sensible
result or raises ValueError. Any other exception (TypeError, OverflowError,
AttributeError ...) or a silently wrong result (nan, wrong channel,
prohibited item let through) is a bug.
"""
import math

from hypothesis import assume, given, strategies as st

from processor import PROHIBITED, clearance_channel, duty_rate, total_duty

# ---------- strategies ----------
# Anything at all: wrong types, nan/inf, huge ints, unhashable lists ...
anything = (
    st.none()
    | st.text()
    | st.integers()
    | st.floats()                       # includes nan, inf, -inf
    | st.booleans()
    | st.binary()
    | st.lists(st.integers())
)
# Valid building blocks
valid_value = st.floats(min_value=0, max_value=1e12, allow_nan=False, allow_infinity=False)
valid_category = st.text(min_size=1).filter(lambda s: s.strip())
known_category = st.sampled_from(["electronics", "clothing", "books", "toys", "Electronics", " CLOTHING "])
prohibited_category = st.sampled_from(
    ["weapons", "narcotics", "Weapons", "NARCOTICS", "  weapons  ", "NarCotics"]
)
origin = st.text() | st.sampled_from(["FTA", "fta", " Fta "])


def norm(c):
    return c.strip().lower()


# ---------- 1. No-crash fuzz tests (one per function) ----------

@given(anything, anything)
def test_duty_rate_no_crash(category, org):
    try:
        duty_rate(category, org)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"duty_rate crashed with: {e!r}"


@given(anything, anything, anything, anything)
def test_total_duty_no_crash(category, value, org, gift):
    try:
        total_duty(category, value, org, gift)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"total_duty crashed with: {e!r}"


@given(anything, anything, anything)
def test_clearance_channel_no_crash(value, category, docs):
    try:
        clearance_channel(value, category, docs)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"clearance_channel crashed with: {e!r}"


# ---------- 2. Result-correctness properties ----------

@given(valid_category, origin)
def test_duty_rate_is_a_known_rate(category, org):
    assume(norm(category) not in PROHIBITED)
    assert duty_rate(category, org) in {0, 0.05, 0.10, 0.12, 0.15, 0.20}


@given(valid_category, valid_value, origin, st.booleans())
def test_total_duty_is_finite_and_non_negative(category, value, org, gift):
    assume(norm(category) not in PROHIBITED)
    d = total_duty(category, value, org, gift)
    assert math.isfinite(d) and d >= 0
    assert d <= max(50, value * 0.20)          # never above top rate / minimum duty


@given(valid_category, valid_value, origin, st.booleans())
def test_total_duty_is_zero_or_at_least_minimum(category, value, org, gift):
    assume(norm(category) not in PROHIBITED)
    d = total_duty(category, value, org, gift)
    assert d == 0 or d >= 50


@given(known_category, st.floats(min_value=0, max_value=1000, allow_nan=False), origin)
def test_small_personal_imports_are_duty_free(category, value, org):
    assert total_duty(category, value, org, False) == 0


@given(known_category, st.floats(min_value=0, max_value=5000, allow_nan=False), origin)
def test_small_gifts_are_duty_free(category, value, org):
    assert total_duty(category, value, org, True) == 0


@given(valid_value, valid_category, st.booleans())
def test_clearance_channel_returns_known_value(value, category, docs):
    assert clearance_channel(value, category, docs) in {"refuse", "inspect", "green"}


@given(st.floats(min_value=100000.01, max_value=1e12), known_category, st.booleans())
def test_very_high_value_is_inspected(value, category, docs):
    assert clearance_channel(value, category, docs) == "inspect"


@given(st.floats(min_value=0, max_value=20000, allow_nan=False), known_category, st.booleans())
def test_low_value_is_green(value, category, docs):
    assert clearance_channel(value, category, docs) == "green"


# ---------- 3. Security-style properties (found by fuzzing) ----------

@given(prohibited_category, origin)
def test_prohibited_items_never_get_a_rate(category, org):
    try:
        duty_rate(category, org)
        assert False, "prohibited item was given a duty rate"
    except ValueError:
        pass


@given(prohibited_category, valid_value, origin, st.booleans())
def test_prohibited_items_never_pass_total_duty(category, value, org, gift):
    # even tiny values / gifts must not slip through the duty-free exemptions
    try:
        total_duty(category, value, org, gift)
        assert False, "prohibited item was let through"
    except ValueError:
        pass


@given(valid_value, prohibited_category, st.booleans())
def test_prohibited_items_are_always_refused(value, category, docs):
    assert clearance_channel(value, category, docs) == "refuse"


@given(st.sampled_from([float("nan"), float("inf"), float("-inf"), -1, -0.01, 10**400]))
def test_bad_numbers_are_rejected_everywhere(bad):
    for call in (
        lambda: total_duty("electronics", bad, "US", False),
        lambda: clearance_channel(bad, "books", True),
    ):
        try:
            call()
            assert False, f"{bad!r} was accepted"
        except ValueError:
            pass


@given(known_category, origin)
def test_category_and_origin_are_case_insensitive(category, org):
    assert duty_rate(category, org) == duty_rate(norm(category), org.strip().upper())
