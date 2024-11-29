from aiogram.filters.state import State, StatesGroup

class Form(StatesGroup):
    set_repair = State()
    set_ads = State()