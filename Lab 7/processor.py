import math

MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,
}


def lookup_drink_code(code_string):
    if not isinstance(code_string, str):
        return None
    code_prefix = code_string.strip().upper()[:3]
    return MENU_PRICES.get(code_prefix)


def calculate_average_shot_cost(pricing_csv):
    if not isinstance(pricing_csv, str):
        return None
    try:
        prices = [float(p) for p in pricing_csv.split(',')]
    except ValueError:
        return None
    if not prices or any(not math.isfinite(p) for p in prices):
        return None
    return sum(prices) / len(prices)


def parse_order_modifiers(order_spec):
    if not isinstance(order_spec, str):
        return None
    modifier_dict = {}
    for item in order_spec.split(';'):
        if not item.strip():
            continue
        if ':' not in item:
            return None
        key, value = item.split(':', 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            return None
        modifier_dict[key] = value
    if not modifier_dict:
        return None
    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    if price is None:
        print("Invalid or unknown drink code.")
    else:
        print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    if avg_price is None:
        print("Invalid shot prices.")
    else:
        print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    if mods is None:
        print("Invalid modifiers. Use key:value pairs separated by ; (e.g. milk:oat;syrup:vanilla).")
    else:
        print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
