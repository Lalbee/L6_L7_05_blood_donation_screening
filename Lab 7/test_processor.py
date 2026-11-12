from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry

@given(st.text() | st.none())
def test_validate_blood_type_no_crash(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_calculate_pulse_pressure_safe(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_donor_registry_safe(s):
    #To-Do:Using try and except complete this function.
    pass