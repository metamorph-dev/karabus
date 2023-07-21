def validate_number_plate(value: str) -> str:
    if not value[:2].isalpha():
        raise ValueError("First 2 characters must be letters")

    if not value[2:6].isdigit():
        raise ValueError("Must be 4 digits in the middle")

    if not value[6:].isalpha():
        raise ValueError("Last 2 characters must be letters")

    return value
