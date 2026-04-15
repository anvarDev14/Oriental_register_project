from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    waiting_for_fullname = State()
    waiting_for_phone = State()
    waiting_for_passport = State()
