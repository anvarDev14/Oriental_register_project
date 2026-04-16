from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)

from app.utils.directions import DIRECTIONS, format_price


def get_phone_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Ro'yxatdan o'tish", callback_data="register")],
            [InlineKeyboardButton(text="👤 Bot egasi", callback_data="bot_owner")],
        ]
    )


def get_registered_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Yana ro'yxatdan o'tish", callback_data="register")],
            [InlineKeyboardButton(text="👤 Bot egasi", callback_data="bot_owner")],
        ]
    )


def get_skip_kb(step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data=f"skip_{step}")]
        ]
    )


def get_direction_kb() -> InlineKeyboardMarkup:
    buttons = []
    for d in DIRECTIONS:
        buttons.append([
            InlineKeyboardButton(
                text=f"{d['id']}. {d['name']}",
                callback_data=f"dir_{d['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_study_type_kb(direction_id: int) -> InlineKeyboardMarkup:
    d = next((x for x in DIRECTIONS if x["id"] == direction_id), None)
    if not d:
        return InlineKeyboardMarkup(inline_keyboard=[])

    buttons = []
    if d["kunduzgi"]:
        buttons.append([InlineKeyboardButton(
            text=f"🌞 Kunduzgi — {format_price(d['kunduzgi'])}",
            callback_data="type_Kunduzgi",
        )])
    if d["kechki"]:
        buttons.append([InlineKeyboardButton(
            text=f"🌙 Kechki — {format_price(d['kechki'])}",
            callback_data="type_Kechki",
        )])
    if d["sirtqi"]:
        buttons.append([InlineKeyboardButton(
            text=f"📚 Sirtqi — {format_price(d['sirtqi'])}",
            callback_data="type_Sirtqi",
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha, roziman", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no"),
            ]
        ]
    )


remove_kb = ReplyKeyboardRemove()
