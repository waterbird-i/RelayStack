from datetime import timedelta


def add_business_days(start, days, holidays=()):
    return start + timedelta(days=days)
