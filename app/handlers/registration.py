from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from app.bot import OWNER_NAME, BANK_ACCOUNT, BANK_NAME, BANK_MFO
from app.states.register import Register
from app.database.requests import add_user
from app.keyboards.user_kb import (
    get_start_kb,
    get_phone_kb,
    get_skip_kb,
    get_direction_kb,
    get_study_type_kb,
    get_confirm_kb,
    remove_kb,
)
from app.utils.validators import (
    validate_fullname,
    validate_phone,
    validate_jshshir,
    validate_passport_id,
    format_phone,
)
from app.utils.directions import DIRECTION_BY_ID, get_price, format_price
from app.utils.contract_pdf import generate_contract, make_contract_number

router = Router()

CONFIRMATION_QUESTIONS = [
    "📋 <b>1-savol:</b>\nUniversitetning ichki tartib-qoidalari va o'quv intizomi bilan tanishdingizmi?",
    "💰 <b>2-savol:</b>\nYillik kontrakt to'lovi miqdori va to'lov tartibi haqida to'liq ma'lumot oldingizmi?",
    "📅 <b>3-savol:</b>\nTo'lovlarni belgilangan muddatlarda o'z vaqtida amalga oshirishga tayyormisiz?",
    "✍️ <b>4-savol:</b>\nShartnoma shartlarini to'liq o'qib chiqdingizmi va barcha shartlarga rozimisiz?",
]


# ── /start ───────────────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Oriental universitetiga xush kelibsiz!\n"
        "Ro'yxatdan o'tish uchun quyidagi tugmani bosing.",
        reply_markup=get_start_kb(),
    )


# ── Bot egasi ────────────────────────────────────────────────
@router.callback_query(F.data == "bot_owner")
async def show_bot_owner(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"👤 <b>Bot egasi:</b>\n\n<b>{OWNER_NAME}</b>")


# ── Ro'yxatdan o'tish boshlash ───────────────────────────────
@router.callback_query(F.data == "register")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 <b>Ro'yxatdan o'tish</b>\n\n"
        "1-qadam: To'liq ismingizni kiriting (F.I.SH).\n\n"
        "<i>Masalan: Aliyev Ali Valiyevich</i>"
    )
    await state.set_state(Register.waiting_for_fullname)
    await callback.answer()


# ── 1-qadam: F.I.SH ─────────────────────────────────────────
@router.message(Register.waiting_for_fullname)
async def process_fullname(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""
    if not validate_fullname(name):
        await message.answer(
            "❌ To'liq ismingizni kiriting (kamida ism va familiya).\n"
            "<i>Masalan: Aliyev Ali Valiyevich</i>"
        )
        return
    await state.update_data(full_name=name)
    await state.set_state(Register.waiting_for_phone)
    await message.answer(
        "✅ Ism qabul qilindi!\n\n"
        "2-qadam: Telefon raqamingizni yuboring.",
        reply_markup=get_phone_kb(),
    )


# ── 2-qadam: Telefon ─────────────────────────────────────────
@router.message(Register.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = format_phone(message.contact.phone_number)
    await state.update_data(phone_number=phone)
    await state.set_state(Register.waiting_for_jshshir)
    await message.answer(f"✅ Telefon: <b>{phone}</b>", reply_markup=remove_kb)
    await message.answer(
        "3-qadam: JSHSHIR raqamingizni kiriting (14 ta raqam).\n"
        "<i>Masalan: 12345678901234</i>\n\n"
        "Yo'q bo'lsa o'tkazib yuboring:",
        reply_markup=get_skip_kb("jshshir"),
    )


@router.message(Register.waiting_for_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not validate_phone(phone):
        await message.answer(
            "❌ Noto'g'ri format. +998XXXXXXXXX ko'rinishida kiriting.",
            reply_markup=get_phone_kb(),
        )
        return
    await state.update_data(phone_number=phone)
    await state.set_state(Register.waiting_for_jshshir)
    await message.answer(
        f"✅ Telefon: <b>{phone}</b>\n\n"
        "3-qadam: JSHSHIR raqamingizni kiriting (14 ta raqam).\n"
        "<i>Masalan: 12345678901234</i>\n\n"
        "Yo'q bo'lsa o'tkazib yuboring:",
        reply_markup=get_skip_kb("jshshir"),
    )


# ── 3-qadam: JSHSHIR ─────────────────────────────────────────
@router.message(Register.waiting_for_jshshir, F.text)
async def process_jshshir(message: Message, state: FSMContext):
    jshshir = message.text.strip()
    if not validate_jshshir(jshshir):
        await message.answer(
            "❌ JSHSHIR noto'g'ri. Aniq <b>14 ta raqam</b> kiriting.",
            reply_markup=get_skip_kb("jshshir"),
        )
        return
    await state.update_data(jshshir=jshshir)
    await _ask_passport(message, state)


@router.callback_query(Register.waiting_for_jshshir, F.data == "skip_jshshir")
async def skip_jshshir(callback: CallbackQuery, state: FSMContext):
    await state.update_data(jshshir=None)
    await callback.answer()
    await _ask_passport(callback.message, state)


async def _ask_passport(message: Message, state: FSMContext):
    await state.set_state(Register.waiting_for_passport_id)
    await message.answer(
        "4-qadam: Pasport seriyasi va raqamini kiriting.\n"
        "<i>Masalan: AB1234567</i>\n\n"
        "Yo'q bo'lsa o'tkazib yuboring:",
        reply_markup=get_skip_kb("passport"),
    )


# ── 4-qadam: Pasport ─────────────────────────────────────────
@router.message(Register.waiting_for_passport_id, F.text)
async def process_passport_id(message: Message, state: FSMContext):
    passport_id = message.text.strip().upper()
    if not validate_passport_id(passport_id):
        await message.answer(
            "❌ Noto'g'ri format. <b>2 harf + 7 raqam</b> kiriting.\n"
            "<i>Masalan: AB1234567</i>",
            reply_markup=get_skip_kb("passport"),
        )
        return
    await state.update_data(passport_id=passport_id)
    await _ask_direction(message, state)


@router.callback_query(Register.waiting_for_passport_id, F.data == "skip_passport")
async def skip_passport(callback: CallbackQuery, state: FSMContext):
    await state.update_data(passport_id=None)
    await callback.answer()
    await _ask_direction(callback.message, state)


async def _ask_direction(message: Message, state: FSMContext):
    await state.set_state(Register.waiting_for_direction)
    await message.answer(
        "5-qadam: Ta'lim yo'nalishini tanlang:",
        reply_markup=get_direction_kb(),
    )


# ── 5-qadam: Yo'nalish ───────────────────────────────────────
@router.callback_query(Register.waiting_for_direction, F.data.startswith("dir_"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    direction_id = int(callback.data.split("_")[1])
    d = DIRECTION_BY_ID.get(direction_id)
    if not d:
        await callback.answer("Noto'g'ri tanlov.", show_alert=True)
        return
    await state.update_data(direction_id=direction_id, direction_name=d["name"])
    await state.set_state(Register.waiting_for_study_type)
    await callback.message.edit_text(
        f"✅ Yo'nalish: <b>{d['name']}</b>\n\n"
        "6-qadam: Ta'lim shaklini tanlang:",
        reply_markup=get_study_type_kb(direction_id),
    )
    await callback.answer()


# ── 6-qadam: Ta'lim shakli ───────────────────────────────────
@router.callback_query(Register.waiting_for_study_type, F.data.startswith("type_"))
async def process_study_type(callback: CallbackQuery, state: FSMContext):
    study_type = callback.data.replace("type_", "")  # "Kunduzgi" yoki "Kechki"
    await state.update_data(study_type=study_type, confirm_step=0)
    await state.set_state(Register.waiting_for_confirmation)
    await callback.answer()
    await callback.message.answer(
        "📝 <b>Shartnomani tasdiqlashdan oldin bir necha savol:</b>\n\n" +
        CONFIRMATION_QUESTIONS[0],
        reply_markup=get_confirm_kb(),
    )


# ── 7-qadam: Tasdiqlash savollari ────────────────────────────
@router.callback_query(Register.waiting_for_confirmation, F.data == "confirm_no")
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "❌ Shartnoma bekor qilindi.\n\n"
        "Qayta urinish uchun /start ni bosing."
    )
    await state.clear()


@router.callback_query(Register.waiting_for_confirmation, F.data == "confirm_yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    step = data.get("confirm_step", 0) + 1

    if step < len(CONFIRMATION_QUESTIONS):
        await state.update_data(confirm_step=step)
        await callback.message.edit_text(
            CONFIRMATION_QUESTIONS[step],
            reply_markup=get_confirm_kb(),
        )
    else:
        await callback.message.edit_text(
            "✅ Barcha savollarga javob berildi. Shartnoma tayyorlanmoqda..."
        )
        await _finish_registration(callback.message, state, tg_id=callback.from_user.id)


# ── Yakunlash ────────────────────────────────────────────────
async def _finish_registration(message: Message, state: FSMContext, tg_id: int):
    data = await state.get_data()
    await state.clear()

    direction_id = data["direction_id"]
    study_type = data["study_type"]
    study_label = "Kunduzgi" if study_type == "Kunduzgi" else "Kechki"
    price_int = get_price(direction_id, study_type)
    price_str = format_price(price_int)

    user = await add_user(
        tg_id=tg_id,
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        jshshir=data.get("jshshir"),
        passport_id=data.get("passport_id"),
        direction=data["direction_name"],
        study_type=study_label,
    )

    await message.answer(
        "🎓 <b>Tabriklaymiz!</b>\n\n"
        "Siz <b>Oriental universiteti</b>ga o'qishga qabul qilindingiz!\n\n"
        f"👤 F.I.SH: <b>{user.full_name}</b>\n"
        f"📱 Telefon: <b>{user.phone_number}</b>\n"
        f"🪪 JSHSHIR: <code>{user.jshshir or '—'}</code>\n"
        f"📄 Pasport: <b>{user.passport_id or '—'}</b>\n"
        f"📚 Yo'nalish: <b>{user.direction}</b>\n"
        f"📋 Ta'lim shakli: <b>{user.study_type}</b>\n"
        f"💰 Yillik to'lov: <b>{price_str}</b>\n\n"
        "📎 Shartnomangiz yuborilmoqda..."
    )

    contract_number = make_contract_number(tg_id)
    pdf_bytes = generate_contract(
        contract_number=contract_number,
        full_name=user.full_name,
        phone=user.phone_number,
        jshshir=user.jshshir or "",
        passport_id=user.passport_id or "",
        direction=user.direction,
        study_type=user.study_type,
        price=price_str,
        bank_account=BANK_ACCOUNT,
        bank_name=BANK_NAME,
        bank_mfo=BANK_MFO,
        date=datetime.now().strftime("%d.%m.%Y"),
    )

    await message.answer_document(
        BufferedInputFile(pdf_bytes, filename=f"shartnoma_{contract_number}.pdf"),
        caption=f"📄 <b>Ta'lim shartnomasi</b>\nShartnoma № <b>{contract_number}</b>",
    )
