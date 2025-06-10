from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    select_language = State()
    complete_registration = State()