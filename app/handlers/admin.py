from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.bot import ADMIN_IDS, bot
from app.database.requests import get_all_users, get_users_count, get_user, delete_user
from app.keyboards.admin_kb import get_admin_kb, get_user_detail_kb, get_back_kb

router = Router()

USERS_PER_PAGE = 10


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ── /admin komandasi ─────────────────────────────────────────
@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Sizda admin huquqi yo'q.")
        return

    count = await get_users_count()
    await message.answer(
        f"🔐 <b>Admin panel</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{count}</b>",
        reply_markup=get_admin_kb(),
    )


# ── Admin panel callback ─────────────────────────────────────
@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Ruxsat yo'q.", show_alert=True)
        return

    count = await get_users_count()
    await callback.message.edit_text(
        f"🔐 <b>Admin panel</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{count}</b>",
        reply_markup=get_admin_kb(),
    )
    await callback.answer()


# ── Barcha foydalanuvchilar ro'yxati ─────────────────────────
@router.callback_query(F.data == "admin_all_users")
async def admin_all_users(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Ruxsat yo'q.", show_alert=True)
        return

    users = await get_all_users()

    if not users:
        await callback.message.edit_text(
            "📭 Hali hech kim ro'yxatdan o'tmagan.",
            reply_markup=get_back_kb(),
        )
        await callback.answer()
        return

    text_lines = ["👥 <b>Barcha foydalanuvchilar:</b>\n"]

    for i, user in enumerate(users, 1):
        passport = "📸" if user.passport_photo_id else "—"
        text_lines.append(
            f"{i}. <b>{user.full_name}</b>\n"
            f"   📱 {user.phone_number} | {passport}\n"
            f"   📅 {user.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"   🆔 <code>{user.tg_id}</code>\n"
        )

    await callback.message.edit_text(
        "\n".join(text_lines),
        reply_markup=get_back_kb(),
    )
    await callback.answer()


# ── Statistika ───────────────────────────────────────────────
@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Ruxsat yo'q.", show_alert=True)
        return

    users = await get_all_users()
    total = len(users)
    with_passport = sum(1 for u in users if u.passport_photo_id)
    without_passport = total - with_passport

    await callback.message.edit_text(
        "📊 <b>Statistika</b>\n\n"
        f"👥 Jami: <b>{total}</b>\n"
        f"📸 Pasportli: <b>{with_passport}</b>\n"
        f"📭 Pasportsiz: <b>{without_passport}</b>",
        reply_markup=get_back_kb(),
    )
    await callback.answer()


# ── Foydalanuvchini o'chirish ────────────────────────────────
@router.callback_query(F.data.startswith("admin_delete_"))
async def admin_delete_user(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Ruxsat yo'q.", show_alert=True)
        return

    tg_id = int(callback.data.split("_")[-1])
    deleted = await delete_user(tg_id)

    if deleted:
        await callback.answer("✅ Foydalanuvchi o'chirildi.", show_alert=True)
    else:
        await callback.answer("❌ Foydalanuvchi topilmadi.", show_alert=True)

    # Admin panelga qaytish
    count = await get_users_count()
    await callback.message.edit_text(
        f"🔐 <b>Admin panel</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{count}</b>",
        reply_markup=get_admin_kb(),
    )
