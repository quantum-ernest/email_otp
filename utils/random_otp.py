import random


def generate_otp() -> str:
    """
    Generate a 6-digit One-Time Password (OTP).

    This function generates a random 6-digit OTP using Python's random module.

    Returns:
        str: A 6-digit OTP as a string.
    """
    return str(random.randint(100000, 999999))
