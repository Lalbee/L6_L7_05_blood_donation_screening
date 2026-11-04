"""Lab 6 - Branch coverage tests for blood_donation_screening.py

Includes every test from the code-coverage file plus tests that force each
decision (if / elif / for / while) to evaluate BOTH True and False, and the
boundary values around the thresholds.

Run:
    coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
    coverage report -m
"""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def make_cohort(donors, registered=True, ctype="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": ctype,
        "fast_track": fast_track,
        "donors": donors,
    }


GOOD = {"age": 25, "weight_kg": 65, "hb": 14.0}
LOW_HB = {"age": 30, "weight_kg": 70, "hb": 11.0}
HIGH_HB = {"age": 30, "weight_kg": 70, "hb": 19.5}
BAD = {"age": 10, "weight_kg": 30, "hb": 10.0}


# =====================================================================
# process_donor_cohort : input validation  (first `if`)
# =====================================================================

def test_single_accepted_donor():                       # starter test
    result = process_donor_cohort([make_cohort([GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_cohorts_not_a_list_raises():                   # isinstance False
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


def test_volume_zero_raises():                          # list OK, volume <= 0
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([GOOD])], 0)


def test_volume_negative_raises():
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([GOOD])], -450)


# =====================================================================
# outer `for cohort` loop and `clinic_registered` check
# =====================================================================

def test_empty_cohort_list_zero_yield():                # outer loop never runs
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_unregistered_cohort_skipped():                 # `continue` branch
    result = process_donor_cohort([make_cohort([GOOD], registered=False)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_registration_key_defaults_to_skipped():
    assert process_donor_cohort([{}], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_registered_cohort_without_donors_key():        # donors default [] -> inner loop never runs
    result = process_donor_cohort([{"clinic_registered": True}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_registered_cohort_with_empty_donor_list():
    result = process_donor_cohort([make_cohort([])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# =====================================================================
# age / weight deferral (`if age < 17 or weight < 50`)
# =====================================================================

def test_underage_donor_deferred():                     # age < 17
    donor = {"age": 16, "weight_kg": 70, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_underweight_donor_deferred():                  # age OK, weight < 50
    donor = {"age": 30, "weight_kg": 49, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_boundary_age_17_weight_50_hb_limits_accepted():
    donors = [
        {"age": 17, "weight_kg": 50, "hb": 12.5},       # exact lower limits
        {"age": 17, "weight_kg": 50, "hb": 18.0},       # exact upper hb limit
    ]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_missing_donor_fields_use_defaults_and_are_deferred():
    result = process_donor_cohort([make_cohort([{}])], 450)   # age 0 -> deferred
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# =====================================================================
# hemoglobin branches (if < 12.5 / elif > 18.0 / else)
# =====================================================================

def test_low_hb_standard_cohort_deferred_no_break():
    result = process_donor_cohort([make_cohort([LOW_HB, GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_hb_just_below_lower_limit_deferred():
    donor = {"age": 30, "weight_kg": 70, "hb": 12.4}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hb_deferred():
    result = process_donor_cohort([make_cohort([HIGH_HB, GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_hb_just_above_upper_limit_deferred():
    donor = {"age": 30, "weight_kg": 70, "hb": 18.1}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# =====================================================================
# high_altitude cohort: low hb resets total and breaks inner loop
# =====================================================================

def test_high_altitude_low_hb_resets_total_and_breaks():
    cohort = make_cohort([GOOD, LOW_HB, GOOD], ctype="high_altitude")
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_good_hb_no_break():
    cohort = make_cohort([GOOD, GOOD], ctype="high_altitude")
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_break_only_exits_inner_loop_next_cohort_still_processed():
    high_alt = make_cohort([GOOD, LOW_HB, GOOD], ctype="high_altitude")
    standard = make_cohort([GOOD])
    result = process_donor_cohort([high_alt, standard], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# =====================================================================
# fast_track bonus
# =====================================================================

def test_fast_track_true_adds_50():
    result = process_donor_cohort([make_cohort([GOOD], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_false_adds_nothing():
    result = process_donor_cohort([make_cohort([GOOD], fast_track=False)], 450)
    assert result["collected_ml"] == 450


def test_fast_track_still_applies_after_high_altitude_break():
    cohort = make_cohort([GOOD, LOW_HB], ctype="high_altitude", fast_track=True)
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_fast_track_ignored_for_unregistered_cohort():
    cohort = make_cohort([GOOD], registered=False, fast_track=True)
    assert process_donor_cohort([cohort], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


# =====================================================================
# final status decision (deferred_count > 4 / total == 0 / accepted)
# =====================================================================

def test_exactly_four_deferrals_not_high_deferral():
    result = process_donor_cohort([make_cohort([BAD] * 4 + [GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_five_deferrals_is_high_deferral():
    result = process_donor_cohort([make_cohort([BAD] * 5 + [GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_high_deferral_takes_priority_over_zero_yield():
    result = process_donor_cohort([make_cohort([BAD] * 5)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_multiple_cohorts_mixed_results_accumulate():
    c1 = make_cohort([GOOD, LOW_HB])
    c2 = make_cohort([GOOD, HIGH_HB], fast_track=True)
    result = process_donor_cohort([c1, c2], 300)
    assert result == {"collected_ml": 650, "status": "ACCEPTED"}


# =====================================================================
# verify_storage_centrifuge
# =====================================================================

def test_centrifuge_no_data_empty_list():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_no_data_none():
    assert verify_storage_centrifuge(None) == "NO_DATA"


def test_centrifuge_stable_all_rpm_ok():
    assert verify_storage_centrifuge([[3500, 3600, 3400]]) == "STABLE"


def test_centrifuge_abort_two_consecutive_drops():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_abort_when_first_two_readings_low():
    assert verify_storage_centrifuge([[2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_single_drop_then_recovery_is_stable():
    assert verify_storage_centrifuge([[3500, 2900, 3500]]) == "STABLE"


def test_centrifuge_streak_resets_so_non_consecutive_drops_are_stable():
    assert verify_storage_centrifuge([[2900, 3500, 2900]]) == "STABLE"


def test_centrifuge_boundary_3000_is_not_a_drop():
    assert verify_storage_centrifuge([[3000, 3000]]) == "STABLE"


def test_centrifuge_boundary_2999_is_a_drop():
    assert verify_storage_centrifuge([[2999, 2999]]) == "ABORT_SPIN"


def test_centrifuge_empty_run_inside_list_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"


def test_centrifuge_streak_does_not_carry_across_runs():
    assert verify_storage_centrifuge([[2900], [2900]]) == "STABLE"


def test_centrifuge_abort_in_later_run():
    assert verify_storage_centrifuge([[3500, 3500], [2900, 2800]]) == "ABORT_SPIN"
