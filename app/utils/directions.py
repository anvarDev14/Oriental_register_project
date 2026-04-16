DIRECTIONS = [
    {"id": 1,  "name": "Filologiya va tillarni o'qitish (Ingliz tili)",          "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 2,  "name": "Filologiya va tillarni o'qitish (Kores tili)",            "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 3,  "name": "Filologiya va tillarni o'qitish (Turk tili)",             "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 4,  "name": "Filologiya va tillarni o'qitish (Xitoy tili)",            "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 5,  "name": "Filologiya va tillarni o'qitish (O'zbek tili)",           "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 6,  "name": "Filologiya va tillarni o'qitish (Rus tili)",              "kunduzgi": 13_600_000, "kechki": 13_600_000, "sirtqi": None},
    {"id": 7,  "name": "Boshlang'ich ta'lim",                                     "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 8,  "name": "Tarix (yo'nalishlar va faoliyat turlari)",                "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 9,  "name": "Pedagogika va psixologiya",                               "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 10, "name": "Maktabgacha ta'lim",                                      "kunduzgi": 11_900_000, "kechki": None,       "sirtqi": 11_900_000},
    {"id": 11, "name": "Jismoniy madaniyat",                                      "kunduzgi": 11_900_000, "kechki": None,       "sirtqi": 11_900_000},
    {"id": 12, "name": "Milliy g'oya, ma'naviyat asoslari va huquq ta'limi",      "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 13, "name": "Matematika va informatika",                               "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 14, "name": "Iqtisodiyot (tarmoqlar va sohalar bo'yicha)",             "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 15, "name": "Buxgalteriya hisobi va audit",                            "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 16, "name": "Moliya va moliyaviy texnologiyalar",                      "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 17, "name": "Bank ishi va auditi",                                     "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 18, "name": "Axborot tizimlari va texnologiyalari",                    "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
    {"id": 19, "name": "Kompyuter injiniringi",                                   "kunduzgi": 13_600_000, "kechki": None,       "sirtqi": 13_600_000},
]

DIRECTION_BY_ID = {d["id"]: d for d in DIRECTIONS}


def get_price(direction_id: int, study_type: str) -> int:
    d = DIRECTION_BY_ID.get(direction_id)
    if not d:
        return 0
    if study_type == "Kunduzgi":
        return d["kunduzgi"] or 0
    if study_type == "Kechki":
        return d["kechki"] or 0
    if study_type == "Sirtqi":
        return d["sirtqi"] or 0
    return 0


def format_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " so'm"
