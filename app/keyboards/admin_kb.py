from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Barcha foydalanuvchilar", callback_data="admin_all_users")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        ]
    )


def get_user_detail_kb(tg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"admin_delete_{tg_id}")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_all_users")],
        ]
    )


def get_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_panel")],
        ]
    )
