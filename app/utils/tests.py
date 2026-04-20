import random

TESTS = [
    {
        "question": "So'zlar orasidan ortiqchasini tanlang.",
        "options": {"A": "Ispaniya", "B": "Fransiya", "C": "Italiya", "D": "Afina"},
        "answer": "D",
    },
    {
        "question": "So'z o'yini to'ldiring: gut, laylak, kostyum, ..., do'rixona",
        "options": {"A": "olmos", "B": "maqsad", "C": "ajrim", "D": "ma'ruza"},
        "answer": "C",
    },
    {
        "question": (
            "Chizg'ich va ruchka uchun jami 1 so'm 10 tiyin to'landi. "
            "Agar chizg'ich ruchkadan 1 so'm qimmat bo'lsa, ruchkaning narxi qancha?"
        ),
        "options": {"A": "5 tiyin", "B": "10 tiyin", "C": "15 tiyin", "D": "95 tiyin"},
        "answer": "A",
    },
    {
        "question": "4=20; 5=30; 6=42; 7=56; 8=?",
        "options": {"A": "72", "B": "50", "C": "32", "D": "68"},
        "answer": "A",
    },
    {
        "question": (
            "Ota va o'g'il oyna tashish jarayonida shunday kelishishdi: 'Har bir tashilgan oyna "
            "uchun 7 so'mdan beraman, har bir singan oyna uchun 12 so'm qaytarib olaman'. "
            "O'g'il 38 ta oyna tashiganidan so'ng hech qanday haq olmadi. "
            "U nechta oynani sindirganini aniqlang."
        ),
        "options": {"A": "32", "B": "25", "C": "14", "D": "24"},
        "answer": "C",
    },
    {
        "question": (
            "Zarina va Madina birgalikda oynani 30 minutda, Madina va Nigora birgalikda "
            "20 minutda, Zarina va Nigora esa birgalikda 12 minutda tozalaydi. "
            "Uchta qiz birgalikda shu vazifani qancha vaqtda bajaradi?"
        ),
        "options": {"A": "16 minut", "B": "37 minut", "C": "15 minut", "D": "12 minut"},
        "answer": "D",
    },
    {
        "question": (
            "Mahbuba 2 xonali bir son o'yladi. Shu sonni raqamlarini o'rnini "
            "o'zgartirganda hosil bo'lgan son o'ylangan sondan 45 ga katta. Sonni aniqlang."
        ),
        "options": {"A": "16", "B": "15", "C": "14", "D": "12"},
        "answer": "A",
    },
    {
        "question": "a32b + 4bca = 7777 bo'lsa, a + b + c = ?",
        "options": {"A": "15", "B": "10", "C": "7", "D": "12"},
        "answer": "D",
    },
    {
        "question": "Quyidagilar orasidan mantiqan ortiqchasini aniqlang.",
        "options": {"A": "baliq", "B": "tovuq", "C": "sigir", "D": "mushuk"},
        "answer": "A",
    },
    {
        "question": (
            "Bu 'mashina' umuman harakatlanish uchun mo'ljallanmagan. Ammo butun dunyodagi "
            "ularning yurgan 'yo'lini' hisoblasak, avtomobil va samolyot bosib o'tgan "
            "masofadan ortib ketadi. 'Mashina'ni aniqlang."
        ),
        "options": {"A": "poyezd", "B": "odam", "C": "soat", "D": "velosiped"},
        "answer": "C",
    },
    {
        "question": "Ikkita tovuq ikki kunda ikkita tuxum beradi. 4 ta tovuq 4 kunda qancha tuxum beradi?",
        "options": {"A": "16", "B": "24", "C": "8", "D": "12"},
        "answer": "A",
    },
    {
        "question": "Ketma-ketlikning keyingi hadini aniqlang: 0, 1, 1, 2, 3, 5, 8, ...",
        "options": {"A": "10", "B": "13", "C": "9", "D": "12"},
        "answer": "B",
    },
    {
        "question": (
            "Ota va o'g'ilning birgalikdagi yoshi 60. "
            "Ota o'g'lidan 40 yosh katta bo'lsa, o'g'il necha yoshda?"
        ),
        "options": {"A": "13", "B": "20", "C": "10", "D": "17"},
        "answer": "C",
    },
    {
        "question": "1 km necha santimetrga teng?",
        "options": {"A": "100", "B": "1 000", "C": "100 000", "D": "10 000"},
        "answer": "C",
    },
    {
        "question": (
            "Agar daraxt kesuvchi 2 ta daraxtni kesish uchun 1 soat vaqt sarflagan bo'lsa, "
            "9 ta xuddi shunday daraxtni kesishi uchun u necha daqiqa vaqt sarfaydi?"
        ),
        "options": {"A": "300", "B": "240", "C": "330", "D": "270"},
        "answer": "D",
    },
    {
        "question": (
            "Shunday butun sonni o'ylangki, u songa 3 ni qo'shib, "
            "yig'indini 12 ga ko'paytirsa, natijada nol hosil bo'lsin. "
            "O'ylagan sonni toping."
        ),
        "options": {"A": "-3", "B": "-12", "C": "-36", "D": "0"},
        "answer": "A",
    },
    {
        "question": (
            "Metall qotishmasi massasining 56% ini mis tashkil qiladi. "
            "3 kg qotishmaning necha grammini mis tashkil qiladi?"
        ),
        "options": {"A": "1 500", "B": "2 130", "C": "1 860", "D": "1 680"},
        "answer": "D",
    },
]


def get_random_tests(n: int = 10) -> list[dict]:
    return random.sample(TESTS, min(n, len(TESTS)))
