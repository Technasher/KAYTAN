from aiogram.fsm.state import StatesGroup, State


class ProgramState(StatesGroup):
    name = State()
    description = State()
    # media = State()
