"""Original starter tests, retained for the baseline measurement."""
from customs_duty import duty_rate, total_duty


def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0
