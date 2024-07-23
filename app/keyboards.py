from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
import config



# ------------------------------ MAIN ------------------------------ #
main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👥 Диалоги 👥', callback_data='dialogues')],
        [InlineKeyboardButton(text='💳 Кошелек 💳', callback_data='wallet')],
        [InlineKeyboardButton(text='⚒ Дополнительно ⚒', callback_data='additional')],
    ]
)

async def get_dialogues_markup(button_texts):
    dialogues = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🟢 {button_texts[0]}", callback_data='dialog_1')],
            [InlineKeyboardButton(text=f"🔵 {button_texts[1]}", callback_data='dialog_2')],
            [InlineKeyboardButton(text=f"🟣 {button_texts[2]}", callback_data='dialog_3')],
            [InlineKeyboardButton(text=f"🟤 {button_texts[3]}", callback_data='dialog_4')],
            [InlineKeyboardButton(text=f"🟠 {button_texts[4]}", callback_data='dialog_5')],
            [InlineKeyboardButton(text='Назад ⬅', callback_data='to_main')],
        ]
    )
    return dialogues

wallet = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Пополнить', callback_data='payment')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_main')]
    ]
)

additional = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🌎 Реферальная программа 🌍', callback_data='referal')],
        [InlineKeyboardButton(text='⚒ Настройки ⚒', callback_data='settings')],
        [InlineKeyboardButton(text='🌐 Информация 🌐', callback_data='info')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_main')]
    ]
)
# ------------------------------ MAIN ------------------------------ #


# ------------------------------ ADDITIONAL ------------------------------ #
referal = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_additional')]
    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Установка пользовательских инструкций', callback_data='first_promt')],
        [InlineKeyboardButton(text='Установка желаемого формата ответа', callback_data='second_promt')],
        [InlineKeyboardButton(text='Установить настройки по умолчанию', callback_data='set_default_settings')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_additional')]
    ]
)

info = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='📧 Модели', callback_data='about_model'), InlineKeyboardButton(text='Токены 💲', callback_data='about_token')],
        [InlineKeyboardButton(text='💬 Промты', callback_data='about_promt'), InlineKeyboardButton(text='Реферальная программа 🆓', callback_data='about_referal')],
        [InlineKeyboardButton(text='🤖 Про бота', callback_data='about_bot'), InlineKeyboardButton(text='Создатели 👤', callback_data='about')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_additional')]
    ]
)
# ------------------------------ ADDITIONAL ------------------------------ #


# ------------------------------ DIALOGUE ------------------------------ #
dialogue_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить название диалога', callback_data='change_name_1'), InlineKeyboardButton(text='Выбрать модель', callback_data='change_model_1')],
        [InlineKeyboardButton(text='Показать историю', callback_data='history_1'), InlineKeyboardButton(text='Отчистить историю', callback_data='del_history_1')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_dialogues')]
    ]
)

dialogue_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить название диалога', callback_data='change_name_2'), InlineKeyboardButton(text='Выбрать модель', callback_data='change_model_2')],
        [InlineKeyboardButton(text='Показать историю', callback_data='history_2'), InlineKeyboardButton(text='Отчистить историю', callback_data='del_history_2')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_dialogues')]
    ]
)

dialogue_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить название диалога', callback_data='change_name_3'), InlineKeyboardButton(text='Выбрать модель', callback_data='change_model_3')],
        [InlineKeyboardButton(text='Показать историю', callback_data='history_3'), InlineKeyboardButton(text='Отчистить историю', callback_data='del_history_3')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_dialogues')]
    ]
)

dialogue_4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить название диалога', callback_data='change_name_4'), InlineKeyboardButton(text='Выбрать модель', callback_data='change_model_4')],
        [InlineKeyboardButton(text='Показать историю', callback_data='history_4'), InlineKeyboardButton(text='Отчистить историю', callback_data='del_history_4')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_dialogues')]
    ]
)

dialogue_5 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить название диалога', callback_data='change_name_5'), InlineKeyboardButton(text='Выбрать модель', callback_data='change_model_5')],
        [InlineKeyboardButton(text='Показать историю', callback_data='history_5'), InlineKeyboardButton(text='Отчистить историю', callback_data='del_history_5')],
        [InlineKeyboardButton(text='Назад ⬅', callback_data='to_dialogues')]
    ]
)

async def get_models_markup(dialogue_number: int):
    marlup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='gpt-4o-mini', callback_data=f"set gpt-4o-mini to dialogue_{dialogue_number}")],
            [InlineKeyboardButton(text='gpt-4o', callback_data=f"set gpt-4o to dialogue_{dialogue_number}")],
        ]
    )
    return marlup
# ------------------------------ DIALOGUE ------------------------------ #
