"""Stage 2: cover both outcomes of each decision and threshold boundaries."""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


@pytest.mark.parametrize("category,origin,expected", [
    ("electronics", "FTA", 0.10), ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05), ("clothing", "US", 0.12),
    ("books", "FTA", 0), ("books", "US", 0),
    ("furniture", "US", 0.15), ("furniture", "FTA", 0.15),
])
def test_rate_branches(category, origin, expected):
    assert duty_rate(category, origin) == expected


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_categories(category):
    with pytest.raises(ValueError, match="^prohibited item$"):
        duty_rate(category, "FTA")
    with pytest.raises(ValueError, match="^prohibited item$"):
        total_duty(category, 1001, "US", False)


@pytest.mark.parametrize("gift", [False, True])
def test_negative_value_branches(gift):
    with pytest.raises(ValueError, match="^negative value$"):
        total_duty("electronics", -1, "US", gift)


@pytest.mark.parametrize("category,value,origin,gift,expected", [
    ("electronics", 0, "US", False, 0),
    ("electronics", 999, "US", False, 0),
    ("electronics", 1000, "US", False, 0),
    ("electronics", 1001, "US", False, 200.2),
    ("electronics", 4999, "US", True, 0),
    ("electronics", 5000, "US", True, 0),
    ("electronics", 5001, "US", True, 50),
    ("electronics", 5249, "US", True, 50),
    ("electronics", 5250, "US", True, 50),
    ("electronics", 5251, "US", True, 50.2),
    ("electronics", 6000, "FTA", True, 100),
    ("books", 1001, "US", False, 0),
    ("books", 5001, "US", True, 0),
    ("clothing", 2000, "FTA", False, 100),
    ("clothing", 2000, "US", False, 240),
    ("furniture", 2000, "US", False, 300),
])
def test_total_branches(category, value, origin, gift, expected):
    assert total_duty(category, value, origin, gift) == pytest.approx(expected)


@pytest.mark.parametrize("value,category,documents,expected", [
    (0, "weapons", True, "refuse"),
    (100001, "narcotics", False, "refuse"),
    (19999, "books", False, "green"),
    (20000, "books", False, "green"),
    (20001, "books", False, "inspect"),
    (20001, "books", True, "green"),
    (99999, "books", True, "green"),
    (100000, "books", True, "green"),
    (100000, "books", False, "inspect"),
    (100001, "books", True, "inspect"),
    (100001, "books", False, "inspect"),
])
def test_clearance_branches(value, category, documents, expected):
    assert clearance_channel(value, category, documents) == expected
