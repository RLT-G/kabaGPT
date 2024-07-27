from aiogram.fsm.state import StatesGroup, State


class Feedback(StatesGroup):
    feedback = State()

class SetFirstPromt(StatesGroup):
    promt = State()

class SetSecondPromt(StatesGroup):
    promt = State()

class Dialogue_1(StatesGroup):
    dialog = State()
    change_name = State()
    change_model = State()

class Dialogue_2(StatesGroup):
    dialog = State()
    change_name = State()
    change_model = State()

class Dialogue_3(StatesGroup):
    dialog = State()
    change_name = State()
    change_model = State()

class Dialogue_4(StatesGroup):
    dialog = State()
    change_name = State()
    change_model = State()

class Dialogue_5(StatesGroup):
    dialog = State()
    change_name = State()
    change_model = State()