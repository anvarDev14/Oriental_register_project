from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    waiting_for_fullname = State()
    waiting_for_phone = State()
    waiting_for_jshshir = State()
    waiting_for_passport_id = State()
    waiting_for_level = State()
    waiting_for_direction = State()
    waiting_for_study_type = State()
    waiting_for_confirmation = State()
    waiting_for_test = State()
