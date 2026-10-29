"""Book parcels, track delivery progress, and calculate shipping costs."""

import secrets
import re
import shutil
import subprocess  # nosec B404 - required for the optional ping helper
import sys
import tempfile
from datetime import date

STATUS_FLOW = (
    "Booked", "Picked Up", "In Transit", "Out for Delivery", "Delivered"
)
PARCELS = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and optionally record its ID in a history list."""
    tracking_id = f"TRK{10001 + len(PARCELS)}"
    PARCELS[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }
    if history is not None:
        history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Move a parcel one step forward, stopping at Delivered."""
    parcel = PARCELS[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Charge 50 for the first kilogram and 30 for each extra kilogram."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Describe a parcel's route and status, or report an unknown ID."""
    try:
        parcel = PARCELS[tracking_id]
    except KeyError:
        return f"Unknown tracking id {tracking_id}"
    route = f"{parcel['sender']} -> {parcel['receiver']}"
    return f"{route}: {STATUS_FLOW[parcel['status']]}"


def is_with_courier(tracking_id):
    """Return whether a parcel is picked up or in transit."""
    status = STATUS_FLOW[PARCELS[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create and return a unique, empty label file safely."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as label:
        return label.name


def ping_hub(hub_address):
    """Ping a hub without interpreting its address as shell code."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.:-]*", hub_address):
        raise ValueError("Invalid hub address")
    ping_executable = shutil.which("ping")
    if ping_executable is None:
        raise FileNotFoundError("ping is unavailable")
    count_flag = "-n" if sys.platform == "win32" else "-c"
    return subprocess.run(  # nosec B603 - validated address, no shell
        [ping_executable, count_flag, "1", hub_address],
        check=True,
        capture_output=True,
    ).stdout


def main():
    """Run the demonstration from the assigned starter program."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(PARCELS[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # Unknown ID
    delivery_otp = 1000 + secrets.randbelow(9000)
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(PARCELS))


if __name__ == "__main__":
    main()

