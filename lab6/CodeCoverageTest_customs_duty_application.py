"""Stage 1: execute every application statement with checked results."""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


@pytest.mark.parametrize("category,origin,expected", [
    ("electronics", "FTA", 0.10), ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05), ("clothing", "US", 0.12),
    ("books", "FTA", 0), ("furniture", "US", 0.15),
])
def test_rates(category, origin, expected):
    assert duty_rate(category, origin) == expected


def test_prohibited_rate():
    with pytest.raises(ValueError, match="^prohibited item$"):
        duty_rate("weapons", "US")


def test_negative_value():
    with pytest.raises(ValueError, match="^negative value$"):
        total_duty("books", -1, "US", False)


@pytest.mark.parametrize("category,value,is_gift,expected", [
    ("books", 500, False, 0),
    ("electronics", 5000, True, 0),
    ("electronics", 5100, True, 50),
    ("electronics", 6000, True, 200),
])
def test_total(category, value, is_gift, expected):
    assert total_duty(category, value, "US", is_gift) == expected


@pytest.mark.parametrize("value,category,documents,expected", [
    (0, "weapons", True, "refuse"),
    (100001, "books", True, "inspect"),
    (20001, "books", False, "inspect"),
    (1000, "books", True, "green"),
])
def test_clearance(value, category, documents, expected):
    assert clearance_channel(value, category, documents) == expected
