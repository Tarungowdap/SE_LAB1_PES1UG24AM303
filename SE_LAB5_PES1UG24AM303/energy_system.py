import json
import os
import ast  # Added for secure evaluation

READINGS_FILE = "meters.json"

def load_meter_data():
    if not os.path.exists(READINGS_FILE):
        return {}
    with open(READINGS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_meter_data():
    with open(READINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(meter_data, f, indent=4)

meter_data = load_meter_data()

def record_reading(meter_id, units):
    if meter_id not in meter_data:
        meter_data[meter_id] = []
    meter_data[meter_id].append(units)
    print(f"Readings stored so far: {len(meter_data[meter_id])}")

def calculate_bill(meter_id, rate_per_unit=5.0):
    if meter_id not in meter_data or not meter_data[meter_id]:
        return 0.0
    total_units = sum(meter_data[meter_id])
    return total_units * rate_per_unit

def detect_spikes(threshold=100.0):
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

    adjustment = input("Extra units for M-01 as an expression (Enter for 0): ") or "0"
    
    # Fixed using ast.literal_eval instead of insecure eval()
    record_reading("M-01", ast.literal_eval(adjustment))
    save_meter_data()

    print(f"Bill M-01 after reload: {calculate_bill('M-01'):.2f}")