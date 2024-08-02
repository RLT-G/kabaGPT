from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.custom_filter import ContainsCallbackData
from app.scripts import count_tokens
from app.api import fetch_chatgpt_response, fetch_dalle_response
import app.keyboards as kb
import app.keyboards as kb

from data.database.query import (
    create_user,
    increment_referral_count,
    get_referral_data,
    set_first_promt,
    set_second_promt,
    get_promts,
    set_default_promts,
    get_dialogue_names,
    create_new_chat,
    set_current_dialog_index,
    get_dialog_data_by_index,
    set_dialog_name,
    get_current_dialog_index,
    set_model,
    del_current_dialogue,
    get_data_for_request,
    get_balance,
    set_balance,
    get_referral_balance,
    get_last_invoice,
    set_last_invoice
)

from data.outputs import answer_texts
import config


router = Router()


class States(StatesGroup):
    first_promt = State()
    second_promt = State()
    feedback = State()
    chat = State()
    change_name = State()
    amount = State()
    

# COMMANDS
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    # https://t.me/chatgpt_kaba_bot?start=test
    args = message.text.split()[1:]
    if args:
        referrer_id = int(args[0])
        await increment_referral_count(id=referrer_id)

    else:
        referrer_id = 0

    await create_user(
        id=int(message.from_user.id),
        firstname=str(message.from_user.first_name), 
        lastname=str(message.from_user.last_name),
        referral_user=referrer_id
    )
            
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('main'), 
        parse_mode='html',
        reply_markup=await kb.main(str(message.from_user.language_code))
    )


@router.message(Command('wallet'))
async def wallet(message: types.Message, state: FSMContext):
    await state.clear()
    balance = await get_balance(id=int(message.from_user.id))
    referral_balance = await get_referral_balance(id=int(message.from_user.id))

    gpt4o_tokens = float(balance) / (
        (float(config.OPENAI_MODEL['gpt-4o']['input']) * config.PRICE_MULTIPLIER + \
              float(config.OPENAI_MODEL['gpt-4o']['output']) * config.PRICE_MULTIPLIER) / 2
        )
    
    gpt4omini_tokens = float(balance) / (
        (float(config.OPENAI_MODEL['gpt-4o-mini']['input']) * config.PRICE_MULTIPLIER + \
              float(config.OPENAI_MODEL['gpt-4o-mini']['output']) * config.PRICE_MULTIPLIER) / 2
        )
    
    dalle3_tokens = float(balance) / (float(config.OPENAI_MODEL['dall-e-3']['Standard']['1024×1024']) * config.PRICE_MULTIPLIER)

    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en')
            .get('wallet')
            .format(balance, referral_balance, int(gpt4o_tokens), int(gpt4omini_tokens), int(dalle3_tokens)), 
        parse_mode='html',
        reply_markup=await kb.wallet(laungage_code=str(message.from_user.language_code))
    )


@router.message(Command('dialogues'))
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    dialogue_names = await get_dialogue_names(id=int(message.from_user.id))

    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('dialogue'), 
        parse_mode='html', 
        reply_markup=await kb.dialogue(laungage_code=str(message.from_user.language_code), dialogue_names=dialogue_names)
    )


@router.message(Command('info'))
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('info'), 
        parse_mode='html', 
        reply_markup=await kb.info(str(message.from_user.language_code))
    )


@router.message(Command('feedback'))
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(States.feedback)
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('feedback_1'), 
        parse_mode='html', 
    )


@router.message(Command('referral'))
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=answer_texts.get(
            str(message.from_user.language_code), 'en')
                .get('referral')
                .format(
                    *await get_referral_data(id=int(message.from_user.id)
                )
        ), 
        parse_mode='html', 
        reply_markup=await kb.referral(str(message.from_user.language_code))
    )


@router.message(Command('settings'))
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('settings'), 
        parse_mode='html', 
        reply_markup=await kb.settings(str(message.from_user.language_code))
    )


# ------------------------------ PAYMENT ------------------------------ #
@router.callback_query(F.data == 'payment_1')
async def wallet(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.amount)

    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('payment_1'),
        parse_mode='html',
    )

    await callback.answer()


@router.message(States.amount)
async def send_invoice_handler(message: types.Message, state: FSMContext):

    amount_text = message.text

    try:
        amount = int(amount_text) * 100
        await set_last_invoice(id=int(message.from_user.id), last_invoice=str(amount))

    except ValueError:
        await message.answer("Введите корректную сумму в рублях.")
        return
    
    await state.update_data(amount=amount)

    await message.answer_invoice(        
        title="Пополнение баланса.",
        description="Пополнение кошелька для использования ИИ.\n Конечная сумма будет переведена в USD",
        payload="Payment",
        provider_token=config.YOUKASSA_TEST_TOKEN,
        currency="rub",
        prices=[
            types.LabeledPrice(
                label='Общая сумма',
                amount=amount
            )
        ],
        max_tip_amount=5000_00,
        suggested_tip_amounts=[100_00, 1000_00, 2500_00, 5000_00],
        # provider_data=...
        # need_name=True,
        # need_phone_number=True,
        # need_email=True,
        # need_shipping_address=True,
        # send_phone_number_to_provider=True,
        # send_email_to_provider=True
        disable_notification=False,
        protect_content=True
    )
    await state.clear()


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def success_payment_handler(message: types.CallbackQuery, state: FSMContext):
    amount = float(await get_last_invoice(id=int(message.from_user.id))) / 100
    
    if amount is None:
        await message.answer("Ошибка: сумма платежа не найдена.")
        return
    
    payment_amount = float(amount) * 0.011657 
    await state.clear()
    
    user_id = int(message.from_user.id)
    balance = float(await get_balance(id=user_id))
    await set_balance(id=user_id, balance=str(balance + payment_amount))
    
    await message.answer(text="Оплата прошла успешно")
# ------------------------------ PAYMENT ------------------------------ #


@router.callback_query(F.data == 'wallet')
async def wallet(callback: types.CallbackQuery):
    balance = await get_balance(id=int(callback.from_user.id))
    referral_balance = await get_referral_balance(id=int(callback.from_user.id))

    gpt4o_tokens = float(balance) / (
        (float(config.OPENAI_MODEL['gpt-4o']['input']) * config.PRICE_MULTIPLIER + \
              float(config.OPENAI_MODEL['gpt-4o']['output']) * config.PRICE_MULTIPLIER) / 2
        )
    
    gpt4omini_tokens = float(balance) / (
        (float(config.OPENAI_MODEL['gpt-4o-mini']['input']) * config.PRICE_MULTIPLIER + \
              float(config.OPENAI_MODEL['gpt-4o-mini']['output']) * config.PRICE_MULTIPLIER) / 2
        )
    
    dalle3_tokens = float(balance) / (float(config.OPENAI_MODEL['dall-e-3']['Standard']['1024×1024']) * config.PRICE_MULTIPLIER)

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('wallet')
            .format(balance, referral_balance, int(gpt4o_tokens), int(gpt4omini_tokens), int(dalle3_tokens)), 
        parse_mode='html',
        reply_markup=await kb.wallet(laungage_code=str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'dialogue')
@router.callback_query(F.data == 'to_dialogue')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    dialogue_names = await get_dialogue_names(id=int(callback.from_user.id))

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('dialogue'), 
        parse_mode='html', 
        reply_markup=await kb.dialogue(laungage_code=str(callback.from_user.language_code), dialogue_names=dialogue_names)
    )


@router.callback_query(F.data == 'create_new_chat')
async def func(callback: types.CallbackQuery):
    chat_name, chat_model = await create_new_chat(id=int(callback.from_user.id))

    await callback.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('create_new_chat')
            .format(chat_name, chat_model),
        show_alert=True
    )
    dialogue_names = await get_dialogue_names(id=int(callback.from_user.id))

    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('dialogue'), 
        parse_mode='html', 
        reply_markup=await kb.dialogue(laungage_code=str(callback.from_user.language_code), dialogue_names=dialogue_names)
    )
    

@router.callback_query(F.data == 'change_name')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.change_name)

    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('change_name_1'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.message(States.change_name)
async def func(message: types.Message, state: FSMContext):
    if len(str(message.text)) <= 40:
        await set_dialog_name(
            id=int(message.from_user.id), 
            dialog_name=str(message.text),
        )
        await message.answer(
            text=answer_texts.get(str(message.from_user.language_code), 'en').get('change_name_2'), 
            parse_mode='html', 
        )
        await state.set_state(States.chat)
    else: 
        await message.answer(
            text=answer_texts.get(str(message.from_user.language_code), 'en').get('change_name_1'), 
            parse_mode='html', 
        )


@router.callback_query(F.data == 'change_model')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('change_model'), 
        parse_mode='html', 
        reply_markup=await kb.change_model(laungage_code=str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'show_history')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        text="Просмотр истории сообщений пока не доступен 😢", 
        parse_mode='html', 
    )


@router.callback_query(F.data == 'payment_2')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        text="Оплата через криптовалюту пока не доступна 😢", 
        parse_mode='html', 
    )


@router.callback_query(F.data == 'set_gpt-4o')
@router.callback_query(F.data == 'set_gpt-4o-mini')
@router.callback_query(F.data == 'set_dall-e-3')
async def func(callback: types.CallbackQuery, state: FSMContext):
    if 'gpt-4o-mini' in str(callback.data):
        await set_model(id=int(callback.from_user.id), model='gpt-4o-mini')

    elif 'gpt-4o' in str(callback.data):
        await set_model(id=int(callback.from_user.id), model='gpt-4o')

    elif 'dall-e-3' in str(callback.data):
        await set_model(id=int(callback.from_user.id), model='dall-e-3')

    current_dialog_index = await get_current_dialog_index(id=int(callback.from_user.id))

    dialogue_model, dialog_title = await get_dialog_data_by_index(
        id=int(callback.from_user.id), 
        dialog_index=current_dialog_index
    )

    await state.set_state(States.chat)

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('inner_dialogue')
            .format(dialogue_model, dialog_title), 
        parse_mode='html', 
        reply_markup= await kb.inner_dialogue(laungage_code=str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'to_current_d')
async def func(callback: types.CallbackQuery, state: FSMContext):
    current_dialog_index = await get_current_dialog_index(id=int(callback.from_user.id))

    dialogue_model, dialog_title = await get_dialog_data_by_index(
        id=int(callback.from_user.id), 
        dialog_index=current_dialog_index
    )

    await state.set_state(States.chat)

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('inner_dialogue')
            .format(dialogue_model, dialog_title), 
        parse_mode='html', 
        reply_markup= await kb.inner_dialogue(laungage_code=str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'del_d')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await del_current_dialogue(id=int(callback.from_user.id))

    dialogue_names = await get_dialogue_names(id=int(callback.from_user.id))

    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('dialogue'), 
        parse_mode='html', 
        reply_markup=await kb.dialogue(laungage_code=str(callback.from_user.language_code), dialogue_names=dialogue_names)
    )


# @router.callback_query('d_' in F.data)
@router.callback_query(ContainsCallbackData(substring='d_'))
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.chat)

    await set_current_dialog_index(
        id=int(callback.from_user.id), 
        current_dialog_index=int(str(callback.data)[-1])
    )
    dialogue_model, dialog_title = await get_dialog_data_by_index(
        id=int(callback.from_user.id), 
        dialog_index=int(str(callback.data)[-1])
    )
    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('inner_dialogue')
            .format(dialogue_model, dialog_title), 
        parse_mode='html', 
        reply_markup= await kb.inner_dialogue(laungage_code=str(callback.from_user.language_code))
    )


@router.message(States.chat)
async def func(message: types.Message, state: FSMContext):
    first_promt, second_promt, dialogue_model = await get_data_for_request(id=int(message.from_user.id))

    c_tokens = await count_tokens(
        prompt=str(message.text),
        instructions=first_promt + second_promt,
    )

    if dialogue_model == 'gpt-4o-mini':
        total_price = float(config.OPENAI_MODEL['gpt-4o-mini']['input']) * c_tokens * config.PRICE_MULTIPLIER + \
            float(config.OPENAI_MODEL['gpt-4o-mini']['output']) * config.MAX_OUTPUT_TOKENS * config.PRICE_MULTIPLIER
        
    elif dialogue_model == 'gpt-4o':
        total_price = float(config.OPENAI_MODEL['gpt-4o']['input']) * c_tokens * config.PRICE_MULTIPLIER + \
            float(config.OPENAI_MODEL['gpt-4o']['output']) * config.MAX_OUTPUT_TOKENS * config.PRICE_MULTIPLIER
        
    elif dialogue_model == 'dall-e-3':
        total_price = float(config.OPENAI_MODEL['dall-e-3']['Standard']['1024×1024']) * config.PRICE_MULTIPLIER

    balance = float(await get_balance(id=int(message.from_user.id)))

    if total_price > balance:
        await message.answer(
            text=answer_texts.get(str(message.from_user.language_code), 'en').get('not_enough_money'), 
            parse_mode='html', 
        )
    else:
        try:
            sent_message = await message.answer(
                text="Обработка запроса...", 
                parse_mode='html', 
            )

            if dialogue_model == 'dall-e-3':
                link = await fetch_dalle_response(prompt=str(message.text))
                await sent_message.delete()
                # await message.answer(
                #     text=f"Входноых токенов токенов: {c_tokens}\n{link}", 
                #     parse_mode='html', 
                # )
                await message.answer_photo(photo=link)
            else:

                response = await fetch_chatgpt_response(
                    model=str(dialogue_model),
                    prompt=str(message.text),
                    instructions=first_promt + second_promt
                )

                # response = f'price: {total_price} balance: {balance}\nОтввет от GPT авно выяснено, что при оценке дизайна и композиции читаемый текст мешает сосредоточиться. Lorem Ipsum используют потому, что тот обеспечивает более или менее стандартное заполнение шаблона, а также реальное распределение букв и пробелов в абзацах, которое не получается при простой дубликации "Здесь ваш текст.. Здесь ваш текст.. Здесь ваш текст.." Многие программы электронной вёрстки и редакторы HTML используют Lorem Ipsum в качестве текста по умолчанию, так что поиск по ключевым словам "lorem ipsum" сразу показывает, как много веб-страниц всё ещё дожидаются своего настоящего рождения. За прошедшие годы текст Lorem Ipsum получил много версий. Некоторые версии появились по ошибке, некоторые - намеренно (например, юмористические варианты).'

                await sent_message.delete()
                await message.answer(
                    text=f"Входноых токенов токенов: {c_tokens}\n{response}", 
                    parse_mode='html', 
                )
                await set_balance(id=int(message.from_user.id), balance=str(balance - total_price))

        except Exception as ex:
            print(f'Ошибка в обработке запроса к OpenAI, {ex}')


@router.callback_query(F.data == 'more')
@router.callback_query(F.data == 'to_more')
async def func(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('more'), 
        parse_mode='html', 
        reply_markup=await kb.more(str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'info')
async def func(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('info'), 
        parse_mode='html', 
        reply_markup=await kb.info(str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'feedback')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.feedback)
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('feedback_1'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.message(States.feedback)
async def func(message: types.Message, state: FSMContext):
    await state.clear()
    for admin_id in config.ADMIN_CHAT_IDS:
        try:
            await message.forward(chat_id=int(admin_id))
        except Exception as e:
            print(f"Failed to forward message to admin {admin_id}: {e}")

    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('feedback_2'), 
        parse_mode='html', 
    )


@router.callback_query(F.data == 'token')
async def func(callback: types.CallbackQuery):
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('token'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.callback_query(F.data == 'settings_ai')
async def func(callback: types.CallbackQuery):
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('settings_ai'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.callback_query(F.data == 'usage_ai')
async def func(callback: types.CallbackQuery):
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('usage_ai'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.callback_query(F.data == 'actual_ai')
async def func(callback: types.CallbackQuery):
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('actual_ai'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.callback_query(F.data == 'bot_benefit')
async def func(callback: types.CallbackQuery):
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('bot_benefit'), 
        parse_mode='html', 
    )
    await callback.answer()


@router.callback_query(F.data == 'referral')
async def func(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=answer_texts.get(
            str(callback.from_user.language_code), 'en')
                .get('referral')
                .format(
                    *await get_referral_data(id=int(callback.from_user.id)
                )
        ), 
        parse_mode='html', 
        reply_markup=await kb.referral(str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'settings')
async def func(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('settings'), 
        parse_mode='html', 
        reply_markup=await kb.settings(str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'to_main')
async def func(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('main'), 
        parse_mode='html',
        reply_markup=await kb.main(str(callback.from_user.language_code))
    )


@router.callback_query(F.data == 'first_promt')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.first_promt)
    
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('first_promt'), 
        parse_mode='html',
    )
    await callback.answer()


@router.message(States.first_promt)
async def func(message: types.Message, state: FSMContext):
    await set_first_promt(id=int(message.from_user.id), first_promt=str(message.text))
    await state.clear()
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('first_promt_ok'), 
        parse_mode='html',
    )


@router.callback_query(F.data == 'second_promt')
async def func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.second_promt)
    
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('second_promt'), 
        parse_mode='html',
    )
    await callback.answer()


@router.message(States.second_promt)
async def func(message: types.Message, state: FSMContext):
    await set_second_promt(id=int(message.from_user.id), second_promt=str(message.text))
    await state.clear()
    await message.answer(
        text=answer_texts.get(str(message.from_user.language_code), 'en').get('second_promt_ok'), 
        parse_mode='html',
    )


@router.callback_query(F.data == 'see_promts')
async def func(callback: types.CallbackQuery):
    
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en')
            .get('see_promts')
            .format(*await get_promts(id=int(callback.from_user.id))
        )
    )
    await callback.answer()


@router.callback_query(F.data == 'set_default_promt')
async def func(callback: types.CallbackQuery):
    await set_default_promts(id=int(callback.from_user.id))
    await callback.message.answer(
        text=answer_texts.get(str(callback.from_user.language_code), 'en').get('set_default_promt'),
        parse_mode='html',
    )
    await callback.answer()
