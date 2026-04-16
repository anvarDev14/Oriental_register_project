DIRECTIONS = [
    {"id": 1,  "name": "Filologiya va tillarni o'qitish (O'zbek tili)",     "kunduzgi": 17_000_000, "sirtqi": 14_000_000},
    {"id": 2,  "name": "Filologiya va tillarni o'qitish (Ingliz tili)",      "kunduzgi": 17_000_000, "sirtqi": 14_000_000},
    {"id": 3,  "name": "Filologiya va tillarni o'qitish (Rus/Fors tili)",    "kunduzgi": 15_000_000, "sirtqi": 13_000_000},
    {"id": 4,  "name": "Boshlang'ich ta'lim",                                "kunduzgi": 16_000_000, "sirtqi": 14_000_000},
    {"id": 5,  "name": "Maktabgacha ta'lim",                                 "kunduzgi": 14_000_000, "sirtqi": 12_000_000},
    {"id": 6,  "name": "Pedagogika va psixologiya",                          "kunduzgi": 15_000_000, "sirtqi": 13_000_000},
    {"id": 7,  "name": "Tarix (yo'nalishlar bo'yicha)",                      "kunduzgi": 15_000_000, "sirtqi": 13_000_000},
    {"id": 8,  "name": "Iqtisodiyot (tarmoqlar va sohalar bo'yicha)",        "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 9,  "name": "Moliya va moliyaviy texnologiyalar",                  "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 10, "name": "Buxgalteriya hisobi va audit",                       "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 11, "name": "Bank ishi va auditi",                                "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 12, "name": "Biznesni boshqarish (MBA/BBA)",                      "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 13, "name": "Axborot tizimlari va texnologiyalari",               "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 14, "name": "Kompyuter injiniringi (AT-Servis/Multimedia)",       "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 15, "name": "Sun'iy intellekt",                                   "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 16, "name": "Xalqaro munosabatlar",                               "kunduzgi": 17_000_000, "sirtqi": 15_000_000},
    {"id": 17, "name": "Sport faoliyati (kurash, futbol va h.k.)",           "kunduzgi": 12_000_000, "sirtqi": 10_000_000},
    {"id": 18, "name": "Jismoniy madaniyat",                                 "kunduzgi": 13_000_000, "sirtqi": 11_000_000},
]

DIRECTION_BY_ID = {d["id"]: d for d in DIRECTIONS}


def get_price(direction_id: int, study_type: str) -> int:
    d = DIRECTION_BY_ID.get(direction_id)
    if not d:
        return 0
    return d["kunduzgi"] if study_type == "Kunduzgi" else d["sirtqi"]


def format_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " so'm"
