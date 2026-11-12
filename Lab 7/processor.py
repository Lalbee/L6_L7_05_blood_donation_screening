def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Assumes non-empty string with ABO antigen and +/- sign.
    """
    cleaned = blood_code.strip().upper()
    antigen = cleaned[:-1]
    rh_char = cleaned[-1]
    rh_map = {"+": "Positive", "-": "Negative"}
    return f"{antigen} {rh_map[rh_char]}"

def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Assumes string format 'systolic/diastolic' (e.g. '120/80').
    """
    sys_str, dia_str = bp_string.split('/')
    systolic = int(sys_str)
    diastolic = int(dia_str)
    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"

def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Assumes valid 3-token pipe-separated string.
    """
    fields = donor_entry.split('|')
    donor_id = fields[0].strip()
    weight = float(fields[1])
    hemoglobin = float(fields[2])
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"

def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))

if __name__ == "__main__":
    main()