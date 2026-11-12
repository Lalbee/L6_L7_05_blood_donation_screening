import math

def validate_blood_type(blood_code):
    """Standardizes blood group and Rh factor (e.g. 'O+', 'AB-')."""
    if not isinstance(blood_code, str):
        return "Invalid blood type"
    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return "Invalid blood type"
    antigen, rh_char = cleaned[:-1], cleaned[-1]
    rh_map = {"+": "Positive", "-": "Negative"}
    if antigen not in {"A", "B", "AB", "O"} or rh_char not in rh_map:
        return "Invalid blood type"
    return f"{antigen} {rh_map[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """Calculates pulse pressure (systolic - diastolic) and arterial ratio."""
    if not isinstance(bp_string, str):
        return "Invalid BP"
    parts = bp_string.split('/')
    if len(parts) != 2:
        return "Invalid BP"
    try:
        systolic = int(parts[0])
        diastolic = int(parts[1])
    except (ValueError, OverflowError):
        return "Invalid BP"
    if not (0 < diastolic <= 300 and 0 < systolic <= 300):
        return "Invalid BP"
    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'."""
    if not isinstance(donor_entry, str):
        return "Invalid record"
    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid record"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid record"
    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except ValueError:
        return "Invalid record"
    if not (math.isfinite(weight) and math.isfinite(hemoglobin)) or weight <= 0 or hemoglobin <= 0:
        return "Invalid record"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"