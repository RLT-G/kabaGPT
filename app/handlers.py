from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from .states import *

from database.query import (
    create_user,
    all_users,
    set_default,
    set_first_promt,
    set_second_promt,
    get_button_texts,
    get_dialogue_models,
    set_dialogue_title,
    set_model_to_dialogue,
    add_referral_user,
    get_referral_count
)

import app.keyboards as kb
from app.keyboards import get_dialogues_markup
from app import answers
import config


router = Router()


# COMMANDS
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await create_user(
        id=int(message.from_user.id),
        chat_id=int(message.chat.id),
        firstname=str(message.from_user.first_name), 
        lastname=str(message.from_user.last_name)
    )
    # https://t.me/Kaba_kaba_bot?start=test
    args = message.text.split()[1:]
    if args:
        referrer_id = int(args[0])
        await add_referral_user(referral_id=referrer_id, id=int(message.from_user.id))
            
    await message.answer(text=answers.START_ANSWER, parse_mode='html', reply_markup=kb.main)


# CALLBACKS
# ------------------------------ PAYMENT ------------------------------ #
@router.message(Command('donate'))
async def send_invoice_handler(message: types.Message):
    prices = [types.LabeledPrice(label="XTR", amount=1)]
    await message.answer_invoice(
        title="Оплата услуг",
        description="описание",
        prices=prices,
        provider_token="",
        payload="payload",
        currency="XTR",
        reply_markup=kb.payment_keyboard(amount=1)
    )

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.callback_query(F.successful_payment)
async def success_payment_handler(message: types.Message):
    await message.answer(text="Все шик")

@router.message(Command('paysupport'))
async def pay_support_handler(message: types.Message):  
    await message.answer(  
        text="Добровольные пожертвования не подразумевают возврат средств, "  
        "однако, если вы очень хотите вернуть средства - свяжитесь с нами.")
# ------------------------------ PAYMENT ------------------------------ #


# ------------------------------ MAIN ------------------------------ #
@router.callback_query(F.data == 'dialogues')
async def dialogues(callback: types.CallbackQuery):
    button_texts = await get_button_texts(id=int(callback.from_user.id))
    murkup = await get_dialogues_markup(button_texts=button_texts)
    await callback.message.edit_text(text=answers.DIALOGUES_ANSWER, parse_mode='html', reply_markup=murkup)

@router.callback_query(F.data == 'wallet')
async def wallet(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.WALLET_ANSWER, parse_mode='html', reply_markup=kb.wallet)

@router.callback_query(F.data == 'additional')
async def additional(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.ADDITIONAL_ANSWER, parse_mode='html', reply_markup=kb.additional)
# ------------------------------ MAIN ------------------------------ #


# ------------------------------ ADDITIONAL ------------------------------ #
@router.callback_query(F.data == 'referal')
async def referal(callback: types.CallbackQuery):
    referral_href = f"{config.BOT_BASE_LINK}?start={callback.from_user.id}"
    referal_count = await get_referral_count(id=int(callback.from_user.id))
    await callback.message.edit_text(text=answers.REFERAL_ANSWER.format(referal_count, referral_href), parse_mode='html', reply_markup=kb.referal)

@router.callback_query(F.data == 'settings')
async def settings(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.SETTINGS_ANSWER, parse_mode='html', reply_markup=kb.settings)

@router.callback_query(F.data == 'info')
async def info(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.INFO_ANSWER, parse_mode='html', reply_markup=kb.info)

@router.callback_query(F.data == 'feedback')
async def feedback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Feedback.feedback)
    await callback.message.edit_text(text=answers.FEEDBACK_1, parse_mode='html')
# ------------------------------ ADDITIONAL ------------------------------ #


# ------------------------------ SETTINGS ------------------------------ #
@router.callback_query(F.data == 'set_default_settings')
async def set_default_settings(callback: types.CallbackQuery):
    await set_default(id=int(callback.from_user.id))
    await callback.answer(text='Установлены настройки по умолчанию.', show_alert=True)
# ------------------------------ SETTINGS ------------------------------ #


# ------------------------------ DIALOGUE ------------------------------ #
@router.callback_query(F.data == 'dialog_1')
async def dialog_1(callback: types.CallbackQuery, state: FSMContext):
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=0)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_1.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_1)

@router.callback_query(F.data == 'change_name_1')
async def change_name_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_1.change_name)
    await callback.message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')

@router.callback_query(F.data == 'change_model_1')
async def change_model_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_1.change_model)
    markup = await kb.get_models_markup(dialogue_number=1)
    await callback.message.edit_text(text=answers.CHOUSE_MODEL, reply_markup=markup)

@router.callback_query(F.data == 'dialog_2')
async def dialog_2(callback: types.CallbackQuery, state: FSMContext):
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=1)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_2.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_2)

@router.callback_query(F.data == 'change_name_2')
async def change_name_2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_2.change_name)
    await callback.message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')

@router.callback_query(F.data == 'change_model_2')
async def change_model_2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_2.change_model)
    markup = await kb.get_models_markup(dialogue_number=2)
    await callback.message.edit_text(text=answers.CHOUSE_MODEL, reply_markup=markup)

@router.callback_query(F.data == 'dialog_3')
async def dialog_3(callback: types.CallbackQuery, state: FSMContext):
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=2)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_3.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_3)

@router.callback_query(F.data == 'change_name_3')
async def change_name_3(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_3.change_name)
    await callback.message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')

@router.callback_query(F.data == 'change_model_3')
async def change_model_3(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_3.change_model)
    markup = await kb.get_models_markup(dialogue_number=3)
    await callback.message.edit_text(text=answers.CHOUSE_MODEL, reply_markup=markup)

@router.callback_query(F.data == 'dialog_4')
async def dialog_4(callback: types.CallbackQuery, state: FSMContext):
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=3)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_4.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_4)

@router.callback_query(F.data == 'change_name_4')
async def change_name_4(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_4.change_name)
    await callback.message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')

@router.callback_query(F.data == 'change_model_4')
async def change_model_4(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_4.change_model)
    markup = await kb.get_models_markup(dialogue_number=4)
    await callback.message.edit_text(text=answers.CHOUSE_MODEL, reply_markup=markup)

@router.callback_query(F.data == 'dialog_5')
async def dialog_5(callback: types.CallbackQuery, state: FSMContext):
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=4)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_5.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_5)

@router.callback_query(F.data == 'change_name_5')
async def change_name_5(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_5.change_name)
    await callback.message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')

@router.callback_query(F.data == 'change_model_5')
async def change_model_5(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Dialogue_5.change_model)
    markup = await kb.get_models_markup(dialogue_number=5)
    await callback.message.edit_text(text=answers.CHOUSE_MODEL, reply_markup=markup)

@router.callback_query(F.data == 'history_1')
@router.callback_query(F.data == 'history_2')
@router.callback_query(F.data == 'history_3')
@router.callback_query(F.data == 'history_4')
@router.callback_query(F.data == 'history_5')
async def change_model_5(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="История сообщений пуста")

@router.callback_query(F.data == 'del_history_1')
@router.callback_query(F.data == 'del_history_2')
@router.callback_query(F.data == 'del_history_3')
@router.callback_query(F.data == 'del_history_4')
@router.callback_query(F.data == 'del_history_5')
async def change_model_5(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=answers.HISTORY_IS_DELETED)
# ------------------------------ DIALOGUE ------------------------------ #


# ------------------------------ INFO ------------------------------ #
@router.callback_query(F.data == 'about_bot')
async def about_model(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_BOT)

@router.callback_query(F.data == 'about_stars')
async def about_token(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_STARS, parse_mode='html')

@router.callback_query(F.data == 'about_buy_stars')
async def about_promt(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_BUY_STARS, parse_mode='html')

@router.callback_query(F.data == 'about_actual_model')
async def about_referal(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_ACTUAL_MODEL, parse_mode='html')

@router.callback_query(F.data == 'about_model')
async def about_bot(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_MODEL, parse_mode='html')

@router.callback_query(F.data == 'about_token')
async def about(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_TOKEN, parse_mode='html')

@router.callback_query(F.data == 'about_promt')
async def about(callback: types.CallbackQuery):
    await callback.message.answer(text=answers.ABOUT_PROMT, parse_mode='html')
# ------------------------------ INFO ------------------------------ #


# RETURN CALLBACKS
@router.callback_query(F.data == 'to_main')
async def to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.START_ANSWER, parse_mode='html', reply_markup=kb.main)

@router.callback_query(F.data == 'to_additional')
async def to_additional(callback: types.CallbackQuery):
    await callback.message.edit_text(text=answers.ADDITIONAL_ANSWER, parse_mode='html', reply_markup=kb.additional)
    
@router.callback_query(F.data == 'to_dialogues')
async def to_dialogues(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    button_texts = await get_button_texts(id=int(callback.from_user.id))
    murkup = await get_dialogues_markup(button_texts=button_texts)
    await callback.message.edit_text(text=answers.DIALOGUES_ANSWER, parse_mode='html', reply_markup=murkup)


# ------------------------------ DIALOGUES FSM ------------------------------ #
@router.message(Dialogue_1.dialog)
async def fsm_dialogue_1(message: types.Message, state: FSMContext):
    await message.answer(text="В настройках бота указан не действительный OpenAI токен")

@router.message(Dialogue_2.dialog)
async def fsm_dialogue_2(message: types.Message, state: FSMContext):
    await message.answer(text="В настройках бота указан не действительный OpenAI токен")

@router.message(Dialogue_3.dialog)
async def fsm_dialogue_3(message: types.Message, state: FSMContext):
    await message.answer(text="В настройках бота указан не действительный OpenAI токен")

@router.message(Dialogue_4.dialog)
async def fsm_dialogue_4(message: types.Message, state: FSMContext):
    await message.answer(text="В настройках бота указан не действительный OpenAI токен")

@router.message(Dialogue_5.dialog)
async def fsm_dialogue_5(message: types.Message, state: FSMContext):
    await message.answer(text="В настройках бота указан не действительный OpenAI токен")
# ------------------------------ DIALOGUES FSM ------------------------------ #


# ------------------------------ OTHER FSM ------------------------------ #
@router.message(Feedback.feedback)
async def feedback_fsm(message: types.Message, state: FSMContext):
    await state.clear()
    for admin_id in config.ADMIN_CHAT_IDS:
        try:
            await message.forward(chat_id=int(admin_id))
        except Exception as e:
            print(f"Failed to forward message to admin {admin_id}: {e}")

    await message.answer(text=answers.FEEDBACK_2, parse_mode='html')
    await message.answer(text=answers.ADDITIONAL_ANSWER, parse_mode='html', reply_markup=kb.additional)


@router.callback_query(F.data == 'first_promt')
async def set_first_promt_s1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SetFirstPromt.promt)
    await callback.message.edit_text(text=answers.FIRST_PROMT_TEXT, parse_mode='html')


@router.message(SetFirstPromt.promt)
async def set_first_promt_s2(message: types.Message, state: FSMContext):
    await state.update_data(promt=message.text)
    data = await state.get_data()
    promt = data.get('promt', '')
    await set_first_promt(id=int(message.from_user.id), first_promt=str(promt))
    await state.clear()
    await message.answer(text=answers.SETTINGS_APPLIED)
    await message.answer(text=answers.SETTINGS_ANSWER, parse_mode='html', reply_markup=kb.settings)
    

@router.callback_query(F.data == 'second_promt')
async def set_first_promt_s1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SetSecondPromt.promt)
    await callback.message.edit_text(text=answers.SECOND_PROMT_TEXT, parse_mode='html')


@router.message(SetSecondPromt.promt)
async def set_first_promt_s2(message: types.Message, state: FSMContext):
    await state.update_data(promt=message.text)
    data = await state.get_data()
    promt = data.get('promt', '')
    await set_second_promt(id=int(message.from_user.id), second_promt=str(promt))
    await state.clear()
    await message.answer(text=answers.SETTINGS_APPLIED)
    await message.answer(text=answers.SETTINGS_ANSWER, parse_mode='html', reply_markup=kb.settings)


@router.message(Dialogue_1.change_name)
async def fsm_set_dialog_1_title(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 40:
        await message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')
    else:
        await state.update_data(change_name=message.text)
        data = await state.get_data()
        dialogue_title = data.get('change_name', '')
        dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(message.from_user.id), model_index=0), '')
        await set_dialogue_title(id=int(message.from_user.id), dialogue_title=dialogue_title, dialogue_index=0)
        await state.clear()
        await message.answer(text=answers.SETTINGS_APPLIED)
        await state.set_state(Dialogue_1.dialog)
        await message.answer(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_1)


@router.message(Dialogue_2.change_name)
async def fsm_set_dialog_2_title(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 40:
        await message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')
    else:
        await state.update_data(change_name=message.text)
        data = await state.get_data()
        dialogue_title = data.get('change_name', '')
        dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(message.from_user.id), model_index=0), '')
        await set_dialogue_title(id=int(message.from_user.id), dialogue_title=dialogue_title, dialogue_index=1)
        await state.clear()
        await message.answer(text=answers.SETTINGS_APPLIED)
        await state.set_state(Dialogue_2.dialog)
        await message.answer(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_2)


@router.message(Dialogue_3.change_name)
async def fsm_set_dialog_3_title(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 40:
        await message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')
    else:
        await state.update_data(change_name=message.text)
        data = await state.get_data()
        dialogue_title = data.get('change_name', '')
        dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(message.from_user.id), model_index=0), '')
        await set_dialogue_title(id=int(message.from_user.id), dialogue_title=dialogue_title, dialogue_index=2)
        await state.clear()
        await message.answer(text=answers.SETTINGS_APPLIED)
        await state.set_state(Dialogue_3.dialog)
        await message.answer(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_3)


@router.message(Dialogue_4.change_name)
async def fsm_set_dialog_4_title(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 40:
        await message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')
    else:
        await state.update_data(change_name=message.text)
        data = await state.get_data()
        dialogue_title = data.get('change_name', '')
        dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(message.from_user.id), model_index=0), '')
        await set_dialogue_title(id=int(message.from_user.id), dialogue_title=dialogue_title, dialogue_index=3)
        await state.clear()
        await message.answer(text=answers.SETTINGS_APPLIED)
        await state.set_state(Dialogue_4.dialog)
        await message.answer(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_4)


@router.message(Dialogue_5.change_name)
async def fsm_set_dialog_5_title(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 40:
        await message.answer(text=answers.SET_DIALOGUE_TITLE_TEXT, parse_mode='html')
    else:
        await state.update_data(change_name=message.text)
        data = await state.get_data()
        dialogue_title = data.get('change_name', '')
        dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(message.from_user.id), model_index=0), '')
        await set_dialogue_title(id=int(message.from_user.id), dialogue_title=dialogue_title, dialogue_index=4)
        await state.clear()
        await message.answer(text=answers.SETTINGS_APPLIED)
        await state.set_state(Dialogue_5.dialog)
        await message.answer(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_5)



# SET MODELS
@router.callback_query(F.data == 'set gpt-4o to dialogue_1')
async def set_gpt_4o_to_dialogue_1(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=0, model='gpt-4o')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=0)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_1.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_1)

@router.callback_query(F.data == 'set dalle3 to dialogue_1')
async def set_dalle3_to_dialogue_1(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=0, model='dalle3')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=0)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_1.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_1)

@router.callback_query(F.data == 'set gpt-4o-mini to dialogue_1')
async def set_gpt_4o_mini_to_dialogue_1(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=0, model='gpt-4o-mini')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=0)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=0), '')
    await state.set_state(Dialogue_1.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_1)


@router.callback_query(F.data == 'set gpt-4o-mini to dialogue_2')
async def set_gpt_4o_mini_to_dialogue_2(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=1, model='gpt-4o-mini')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=1)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=1), '')
    await state.set_state(Dialogue_2.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_2)

@router.callback_query(F.data == 'set dalle3 to dialogue_2')
async def set_dalle3_to_dialogue_2(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=1, model='dalle3')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=1)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=1), '')
    await state.set_state(Dialogue_2.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_2)

@router.callback_query(F.data == 'set gpt-4o to dialogue_2')
async def set_gpt_4o_to_dialogue_2(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=1, model='gpt-4o')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=1)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=1), '')
    await state.set_state(Dialogue_2.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_2)


@router.callback_query(F.data == 'set gpt-4o-mini to dialogue_3')
async def set_gpt_4o_mini_to_dialogue_3(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=2, model='gpt-4o-mini')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=2)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=2), '')
    await state.set_state(Dialogue_3.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_3)


@router.callback_query(F.data == 'set dalle3 to dialogue_3')
async def set_dalle3_to_dialogue_3(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=2, model='dalle3')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=2)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=2), '')
    await state.set_state(Dialogue_3.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_3)


@router.callback_query(F.data == 'set gpt-4o to dialogue_3')
async def set_gpt_4o_to_dialogue_3(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=2, model='gpt-4o')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=2)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=2), '')
    await state.set_state(Dialogue_3.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_3)


@router.callback_query(F.data == 'set gpt-4o-mini to dialogue_4')
async def set_gpt_4o_mini_to_dialogue_4(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=3, model='gpt-4o-mini')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=3)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=3), '')
    await state.set_state(Dialogue_4.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_4)

@router.callback_query(F.data == 'set dalle3 to dialogue_4')
async def set_dalle3_to_dialogue_4(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=3, model='dalle3')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=3)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=3), '')
    await state.set_state(Dialogue_4.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_4)

@router.callback_query(F.data == 'set gpt-4o to dialogue_4')
async def set_gpt_4o_to_dialogue_4(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=3, model='gpt-4o')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=3)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=3), '')
    await state.set_state(Dialogue_4.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_4)


@router.callback_query(F.data == 'set gpt-4o-mini to dialogue_5')
async def set_gpt_4o_mini_to_dialogue_5(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=4, model='gpt-4o-mini')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=4)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=4), '')
    await state.set_state(Dialogue_5.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_5)

@router.callback_query(F.data == 'set dalle3 to dialogue_5')
async def set_dalle3_to_dialogue_5(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=4, model='dalle3')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=4)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=4), '')
    await state.set_state(Dialogue_5.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_5)

@router.callback_query(F.data == 'set gpt-4o to dialogue_5')
async def set_gpt_4o_to_dialogue_5(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await set_model_to_dialogue(id=int(callback.from_user.id), dialogue_index=4, model='gpt-4o')
    dialogue_title = await get_button_texts(id=int(callback.from_user.id), dialogue_index=4)
    dialogue_model = answers.PRETTY_MODEL_NAMES.get(await get_dialogue_models(id=int(callback.from_user.id), model_index=4), '')
    await state.set_state(Dialogue_5.dialog)
    await callback.message.edit_text(text=answers.CURENT_DIALOGUES_ANSWER.format(dialogue_title, dialogue_model), parse_mode='html', reply_markup=kb.dialogue_5)
# ------------------------------ OTHER FSM ------------------------------ #
