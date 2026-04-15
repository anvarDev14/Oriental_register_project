import re


def validate_phone(phone: str) -> bool:
    """Telefon raqamni tekshirish: +998XXXXXXXXX formatda"""
    pattern = r"^\+998\d{9}$"
    return bool(re.match(pattern, phone.strip()))


def validate_fullname(name: str) -> bool:
    """F.I.SH tekshirish: kamida 2 so'z, faqat harflar"""
    parts = name.strip().split()
    if len(parts) < 2:
        return False
    return all(part.isalpha() for part in parts)


def format_phone(phone: str) -> str:
    """Telefon raqamni +998XXXXXXXXX formatga keltirish"""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("998"):
        return f"+{digits}"
    if digits.startswith("8") and len(digits) == 10:
        return f"+998{digits[1:]}"
    if len(digits) == 9:
        return f"+998{digits}"
    return f"+{digits}"
