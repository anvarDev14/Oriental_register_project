from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.register import Register
from app.database.requests import get_user, add_user
from app.keyboards.user_kb import (
    get_start_kb,
    get_phone_kb,
    get_skip_kb,
    remove_kb,
)
from app.utils.validators import validate_fullname, validate_phone, format_phone

router = Router()


# ── /start komandasi ──────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            f"👋 Salom, <b>{user.full_name}</b>!\n"
            f"Siz allaqachon ro'yxatdan o'tgansiz.",
        )
        return

    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Botga xush kelibsiz. Ro'yxatdan o'tish uchun quyidagi tugmani bosing.",
        reply_markup=get_start_kb(),
    )


# ── Ro'yxatdan o'tish boshlash ───────────────────────────────
@router.callback_query(F.data == "register")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if user:
        await callback.answer("Siz allaqachon ro'yxatdan o'tgansiz!", show_alert=True)
        return

    await callback.message.edit_text(
        "📝 <b>Ro'yxatdan o'tish</b>\n\n"
        "1-qadam: To'liq ismingizni kiriting (F.I.SH).\n\n"
        "<i>Masalan: Aliyev Ali Valiyevich</i>"
    )
    await state.set_state(Register.waiting_for_fullname)
    await callback.answer()


# ── 1-qadam: F.I.SH qabul qilish ────────────────────────────
@router.message(Register.waiting_for_fullname)
async def process_fullname(message: Message, state: FSMContext):
    name = message.text.strip()

    if not validate_fullname(name):
        await message.answer(
            "❌ Iltimos, to'liq ismingizni kiriting (kamida ism va familiya).\n"
            "<i>Masalan: Aliyev Ali Valiyevich</i>"
        )
        return

    await state.update_data(full_name=name)
    await message.answer(
        "✅ Ism qabul qilindi!\n\n"
        "2-qadam: Telefon raqamingizni yuboring.\n"
        "Quyidagi tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX).",
        reply_markup=get_phone_kb(),
    )
    await state.set_state(Register.waiting_for_phone)


# ── 2-qadam: Telefon raqam qabul qilish ──────────────────────
@router.message(Register.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = format_phone(message.contact.phone_number)
    await state.update_data(phone_number=phone)

    await message.answer(
        f"✅ Telefon raqam qabul qilindi: <b>{phone}</b>\n\n"
        "3-qadam: Pasport rasmini yuboring yoki o'tkazib yuboring.",
        reply_markup=remove_kb,
    )
    await message.answer(
        "📸 Pasport rasmini yuboring:",
        reply_markup=get_skip_kb(),
    )
    await state.set_state(Register.waiting_for_passport)


@router.message(Register.waiting_for_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not validate_phone(phone):
        await message.answer(
            "❌ Noto'g'ri format. Iltimos, +998XXXXXXXXX formatda kiriting\n"
            "yoki tugmani bosib telefon raqamingizni yuboring.",
            reply_markup=get_phone_kb(),
        )
        return

    await state.update_data(phone_number=phone)
    await message.answer(
        f"✅ Telefon raqam qabul qilindi: <b>{phone}</b>\n\n"
        "3-qadam: Pasport rasmini yuboring yoki o'tkazib yuboring.",
        reply_markup=remove_kb,
    )
    await message.answer(
        "📸 Pasport rasmini yuboring:",
        reply_markup=get_skip_kb(),
    )
    await state.set_state(Register.waiting_for_passport)


# ── 3-qadam: Pasport rasmi ───────────────────────────────────
@router.message(Register.waiting_for_passport, F.photo)
async def process_passport_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(passport_photo_id=photo_id)
    await _finish_registration(message, state)


@router.callback_query(Register.waiting_for_passport, F.data == "skip_passport")
async def skip_passport(callback: CallbackQuery, state: FSMContext):
    await state.update_data(passport_photo_id=None)
    await callback.message.edit_text("⏭ Pasport rasmi o'tkazib yuborildi.")
    await _finish_registration(callback.message, state, tg_id=callback.from_user.id)
    await callback.answer()


@router.message(Register.waiting_for_passport)
async def invalid_passport(message: Message, state: FSMContext):
    await message.answer(
        "❌ Iltimos, rasm yuboring yoki \"O'tkazib yuborish\" tugmasini bosing.",
        reply_markup=get_skip_kb(),
    )


# ── Ro'yxatdan o'tishni yakunlash ────────────────────────────
async def _finish_registration(
    message: Message, state: FSMContext, tg_id: int | None = None
):
    data = await state.get_data()
    user_tg_id = tg_id or message.from_user.id

    user = await add_user(
        tg_id=user_tg_id,
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        passport_photo_id=data.get("passport_photo_id"),
    )

    passport_status = "✅ Yuklangan" if user.passport_photo_id else "❌ Yuklanmagan"

    await message.answer(
        "🎉 <b>Ro'yxatdan muvaffaqiyatli o'tdingiz!</b>\n\n"
        f"👤 Ism: <b>{user.full_name}</b>\n"
        f"📱 Telefon: <b>{user.phone_number}</b>\n"
        f"📸 Pasport: {passport_status}\n"
        f"📅 Sana: <b>{user.created_at.strftime('%d.%m.%Y %H:%M')}</b>",
    )
    await state.clear()
