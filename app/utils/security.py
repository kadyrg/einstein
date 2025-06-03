import random


def generate_otp_code() -> str:
    return f"{random.randint(0, 9999):04}"
