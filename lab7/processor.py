import math

PROHIBITED = {"weapons", "narcotics"}

# Contract: every function validates its inputs and signals ANY invalid input
# with ValueError (never TypeError / AttributeError / OverflowError, and never
# a silent nan/inf result).


def _clean_category(category):
    if not isinstance(category, str):
        raise ValueError("category must be a string")
    category = category.strip().lower()      # 'WEAPONS ' must match 'weapons'
    if not category:
        raise ValueError("category must not be empty")
    return category


def _clean_origin(origin):
    if not isinstance(origin, str):
        raise ValueError("origin must be a string")
    return origin.strip().upper()            # 'fta' == 'FTA'


def _clean_value(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("value must be a number")
    try:
        as_float = float(value)              # huge ints raise OverflowError
    except OverflowError:
        raise ValueError("value too large")
    if not math.isfinite(as_float):          # nan / inf
        raise ValueError("value must be finite")
    if as_float < 0:
        raise ValueError("negative value")
    return value


def _clean_flag(flag, name):
    if not isinstance(flag, bool):
        raise ValueError(f"{name} must be a bool")
    return flag


def duty_rate(category, origin):
    category = _clean_category(category)
    origin = _clean_origin(origin)
    if category in PROHIBITED:
        raise ValueError("prohibited item")
    if category == "electronics":
        if origin == "FTA":
            return 0.10
        return 0.20
    if category == "clothing":
        if origin == "FTA":
            return 0.05
        return 0.12
    if category == "books":
        return 0
    return 0.15


def total_duty(category, value, origin, is_gift):
    category = _clean_category(category)
    value = _clean_value(value)
    origin = _clean_origin(origin)
    is_gift = _clean_flag(is_gift, "is_gift")
    # Prohibited items are rejected BEFORE any exemption can return 0.
    if category in PROHIBITED:
        raise ValueError("prohibited item")
    if is_gift:
        if value <= 5000:
            return 0
        value -= 5000
    elif value <= 1000:
        return 0
    duty = value * duty_rate(category, origin)
    if 0 < duty < 50:
        duty = 50
    return duty


def clearance_channel(value, category, has_documents):
    value = _clean_value(value)
    category = _clean_category(category)
    has_documents = _clean_flag(has_documents, "has_documents")
    if category in PROHIBITED:
        return "refuse"
    if value > 100000:
        return "inspect"
    if value > 20000 and not has_documents:
        return "inspect"
    return "green"


def _show(label, fn, *args):
    try:
        print(f"{label:<52} -> {fn(*args)!r}")
    except ValueError as e:
        print(f"{label:<52} -> REJECTED (ValueError: {e})")
    except Exception as e:
        print(f"{label:<52} -> CRASH {type(e).__name__}: {e}")


def main():
    print("==== duty_rate ====")
    _show("duty_rate('electronics', 'FTA')", duty_rate, "electronics", "FTA")
    _show("duty_rate('books', 'US')", duty_rate, "books", "US")
    _show("duty_rate('Electronics', 'fta')", duty_rate, "Electronics", "fta")
    _show("duty_rate('WEAPONS', 'US')", duty_rate, "WEAPONS", "US")
    _show("duty_rate(['x'], 'US')", duty_rate, ["x"], "US")

    print("\n==== total_duty ====")
    _show("total_duty('electronics', 25000, 'US', False)", total_duty, "electronics", 25000, "US", False)
    _show("total_duty('clothing', 300, 'FTA', False)", total_duty, "clothing", 300, "FTA", False)
    _show("total_duty('weapons', 500, 'US', False)", total_duty, "weapons", 500, "US", False)
    _show("total_duty('electronics', float('nan'), 'US', False)", total_duty, "electronics", float("nan"), "US", False)
    _show("total_duty('electronics', None, 'US', False)", total_duty, "electronics", None, "US", False)
    _show("total_duty('electronics', 10**400, 'US', False)", total_duty, "electronics", 10**400, "US", False)
    _show("total_duty('books', 5000, 'US', 'no')", total_duty, "books", 5000, "US", "no")

    print("\n==== clearance_channel ====")
    _show("clearance_channel(15000, 'books', True)", clearance_channel, 15000, "books", True)
    _show("clearance_channel(50000, 'books', False)", clearance_channel, 50000, "books", False)
    _show("clearance_channel(100, 'Narcotics', True)", clearance_channel, 100, "Narcotics", True)
    _show("clearance_channel(float('nan'), 'books', True)", clearance_channel, float("nan"), "books", True)
    _show("clearance_channel(-5, 'books', True)", clearance_channel, -5, "books", True)
    _show("clearance_channel(None, 'books', True)", clearance_channel, None, "books", True)


if __name__ == "__main__":
    main()
