"""Energy Tariff Management System for Lab 5 Static Code Analysis."""

import ast
import json
import os

READINGS_FILE = "meters.json"


def load_meter_data():
    """Load meter data from JSON storage file."""
    if not os.path.exists(READINGS_FILE):
        return {}
    with open(READINGS_FILE, "r", encoding="utf-8") as file_obj:
        try:
            return json.load(file_obj)
        except json.JSONDecodeError:
            return {}


def save_meter_data():
    """Save current meter data to JSON storage file."""
    with open(READINGS_FILE, "w", encoding="utf-8") as file_obj:
        json.dump(meter_data, file_obj, indent=4)


meter_data = load_meter_data()


def record_reading(meter_id, units):
    """Record a new reading for a specific meter ID."""
    if meter_id not in meter_data:
        meter_data[meter_id] = []
    meter_data[meter_id].append(units)
    print(f"Readings stored so far: {len(meter_data[meter_id])}")


def calculate_bill(meter_id, rate_per_unit=5.0):
    """Calculate the total bill for a given meter ID."""
    if meter_id not in meter_data or not meter_data[meter_id]:
        return 0.0
    total_units = sum(meter_data[meter_id])
    return total_units * rate_per_unit


def detect_spikes(threshold=100.0):
    """Detect and return a list of meters that exceeded the threshold."""
    spikes = []
    for m_id, readings in meter_data.items():
        if any(r > threshold for r in readings):
            spikes.append(m_id)
    return spikes


if __name__ == "__main__":
    # Example simulated usage
    record_reading("M-01", 120.0)
    record_reading("M-01", -20.0)
    record_reading("M-01", 395.0)

    record_reading("M-03", -50.0)
    record_reading("M-03", -142.5)

    record_reading("M-02", 50.0)

    print(f"Bill M-01: {calculate_bill('M-01'):.2f}")
    print(f"Bill M-03: {calculate_bill('M-03'):.2f}")
    print(f"Spikes: {detect_spikes(100.0)}")

    adjustment = input(
        "Extra units for M-01 as an expression (Enter for 0): "
    ) or "0"

    # Fixed using ast.literal_eval instead of insecure eval()
    try:
        record_reading("M-01", ast.literal_eval(adjustment))
    except (ValueError, SyntaxError):
        print("Invalid input; no adjustment recorded.")
    save_meter_data()

    print(f"Bill M-01 after reload: {calculate_bill('M-01'):.2f}")
