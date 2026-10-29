import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ---------- Original example test ----------
def test_single_medium_coffee():
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": False,
            "is_member": False,
            "customizations": [{"type": "standard", "cost": 0.5}]
        }
    ]
    result = process_order_batch(orders, 0.1)
    assert result["total"] == 5.5
    assert result["status"] == "COMPLETED"


# ---------- process_order_batch: validation ----------
def test_invalid_orders_type_raises():
    with pytest.raises(ValueError):
        process_order_batch("not a list", 0.1)


# ---------- process_order_batch: order handling ----------
def test_unpaid_order_is_skipped():
    result = process_order_batch([{"paid": False, "size": "small"}], 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_small_size_price():
    result = process_order_batch([{"paid": True, "size": "small"}], 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_large_size_price():
    result = process_order_batch([{"paid": True, "size": "large"}], 0.0)
    assert result == {"total": 6.0, "status": "COMPLETED"}


def test_invalid_size_is_rejected():
    result = process_order_batch([{"paid": True, "size": "xl"}], 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


# ---------- process_order_batch: customizations ----------
def test_negative_cost_modifier_is_rejected():
    orders = [{"paid": True, "size": "small",
               "customizations": [{"type": "extra", "cost": -1.0}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_allergen_alert_strict_voids_item():
    orders = [{"paid": True, "size": "small", "strict_allergy": True,
               "customizations": [{"type": "allergen_alert", "cost": 0.0}]}]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_syrup_cost_is_capped_at_1_50():
    orders = [{"paid": True, "size": "small",
               "customizations": [{"type": "syrup", "cost": 2.0}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


# ---------- process_order_batch: member discount ----------
def test_member_discount_applied():
    orders = [{"paid": True, "size": "medium", "is_member": True}]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == pytest.approx(4.05)
    assert result["status"] == "COMPLETED"


# ---------- process_order_batch: audit ----------
def test_audit_rejected_when_more_than_4_rejections():
    orders = [{"paid": True, "size": "xl"} for _ in range(5)]
    orders.append({"paid": True, "size": "small"})
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "AUDIT_REJECTED"}


# ---------- check_espresso_machine ----------
def test_espresso_no_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_espresso_shutdown_on_two_consecutive_overheats():
    assert check_espresso_machine([[95.0, 97.0, 98.0]]) == "SHUTDOWN"


def test_espresso_optimal():
    assert check_espresso_machine([[90.0, 92.0], [93.0, 94.0]]) == "OPTIMAL"


# =====================================================
# Additional tests for BRANCH coverage
# (each decision is exercised both True and False)
# =====================================================

# ---------- validation: both halves of the "or" condition ----------
def test_negative_tax_rate_raises():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


def test_empty_orders_list_is_no_sale():
    assert process_order_batch([], 0.1) == {"total": 0.0, "status": "NO_SALE"}


# ---------- defaults when keys are missing ----------
def test_missing_paid_key_defaults_to_unpaid():
    assert process_order_batch([{}], 0.1) == {"total": 0.0, "status": "NO_SALE"}


def test_missing_size_defaults_to_medium():
    result = process_order_batch([{"paid": True}], 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


# ---------- customizations ----------
def test_allergen_alert_not_strict_keeps_item():
    orders = [{"paid": True, "size": "small", "strict_allergy": False,
               "customizations": [{"type": "allergen_alert", "cost": 0.0}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_allergen_alert_strict_breaks_out_of_modifier_loop():
    orders = [{"paid": True, "size": "small", "strict_allergy": True,
               "customizations": [{"type": "allergen_alert", "cost": 0.0},
                                  {"type": "extra", "cost": 5.0}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_syrup_cost_under_cap_is_added_fully():
    orders = [{"paid": True, "size": "medium",
               "customizations": [{"type": "syrup", "cost": 1.0}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 5.5, "status": "COMPLETED"}


def test_syrup_cost_exactly_at_cap():
    orders = [{"paid": True, "size": "small",
               "customizations": [{"type": "syrup", "cost": 1.5}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_modifier_with_missing_keys_adds_nothing():
    orders = [{"paid": True, "size": "small", "customizations": [{}]}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


# ---------- member / non-member ----------
def test_non_member_pays_full_price():
    orders = [{"paid": True, "size": "medium", "is_member": False}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


# ---------- audit boundary ----------
def test_exactly_4_rejections_is_not_audit():
    orders = [{"paid": True, "size": "xl"} for _ in range(4)]
    orders.append({"paid": True, "size": "small"})
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_multiple_orders_with_tax():
    orders = [{"paid": True, "size": "small"},
              {"paid": True, "size": "large", "is_member": True},
              {"paid": False, "size": "medium"}]
    result = process_order_batch(orders, 0.1)
    # 3.0 + (6.0 * 0.9) = 8.4 ; 8.4 * 1.1 = 9.24
    assert result == {"total": 9.24, "status": "COMPLETED"}


# ---------- espresso machine ----------
def test_espresso_single_overheat_resets_streak():
    assert check_espresso_machine([[97.0, 90.0, 97.0, 90.0]]) == "OPTIMAL"


def test_espresso_empty_cycle_is_optimal():
    assert check_espresso_machine([[]]) == "OPTIMAL"


def test_espresso_temperature_exactly_96_is_not_overheat():
    assert check_espresso_machine([[96.0, 96.0, 96.0]]) == "OPTIMAL"


def test_espresso_streak_resets_between_cycles():
    # one overheat at the end of cycle 1 and one at the start of cycle 2
    assert check_espresso_machine([[90.0, 97.0], [97.0, 90.0]]) == "OPTIMAL"
