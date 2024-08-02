from data.database.models import async_session
from data.database.models import User
from sqlalchemy import select, update, delete
from config import DEFAULT_VALUES


async def create_user(id: int, firstname: str, lastname: str, referral_user: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id).limit(1))

        if not user:
            session.add(User(
                id=id,
                firstname=firstname,
                lastname=lastname,

                balance=0,
                referral_balance=0,

                first_promt=DEFAULT_VALUES.get('first_promt'),
                second_promt=DEFAULT_VALUES.get('second_promt'),

                referral_user=referral_user
            ))

            await session.commit()


async def get_dialogue_names(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            dialog_titles = str(user.dialog_titles).split(', ')[0:-1]

            return dialog_titles
        

async def get_balance(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            balance = str(user.balance)
            return balance
        

async def get_last_invoice(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            last_invoice = str(user.last_invoice)
            return last_invoice


async def set_last_invoice(id: int, last_invoice: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                last_invoice=last_invoice,
            ))

            await session.commit()


async def get_referral_balance(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            referral_balance = str(user.referral_balance)
            return referral_balance
        

async def set_balance(id: int, balance: str) -> tuple[str]:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                balance=balance,
            ))

            await session.commit()
        

async def create_new_chat(id: int) -> tuple[str]:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            dialog_titles = str(user.dialog_titles)
            dialog_titles += f"{int(len(dialog_titles.split(', ')[0:-1])) + 1}. ChatGPT-4o-mini, "
            dialogue_models = str(user.dialogue_models) + 'gpt-4o-mini, '


            await session.execute(update(User).where(User.id == id).values(
                dialog_titles=dialog_titles,
                dialogue_models=dialogue_models
            ))
            await session.commit()

            return dialogue_models.split(', ')[-2], dialog_titles.split(', ')[-2]


async def increment_referral_count(id: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            referral_count = int(user.referral_count) + 1

            await session.execute(update(User).where(User.id == id).values(
                referral_count=referral_count
            ))
            await session.commit()


async def get_referral_data(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            referral_balance = str(user.referral_balance)
            referral_count = str(user.referral_count)
            referral_link = rf'https://t.me/chatgpt_kaba_bot?start={id}'

            return referral_count, referral_balance, referral_link
        

async def get_promts(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            first_promt = str(user.first_promt)
            second_promt = str(user.second_promt)

            return first_promt, second_promt
        

async def get_data_for_request(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            current_dialog_index = int(user.current_dialog_index)
            first_promt = str(user.first_promt)
            second_promt = str(user.second_promt)
            dialogue_model = str(user.dialogue_models).split(', ')[0:-1][current_dialog_index]

            return first_promt, second_promt, dialogue_model
        

async def get_current_dialog_index(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            current_dialog_index = int(user.current_dialog_index)

            return current_dialog_index


async def get_dialog_data_by_index(id: int, dialog_index: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            dialog_title = str(user.dialog_titles).split(', ')[0:-1][dialog_index]
            dialogue_model = str(user.dialogue_models).split(', ')[0:-1][dialog_index]

            return dialogue_model, dialog_title
        

async def set_model(id: int, model: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            current_dialog_index = int(user.current_dialog_index)
            dialogue_models = str(user.dialogue_models).split(', ')[0:-1]
            dialogue_models[current_dialog_index] = model
            dialogue_models = ', '.join(dialogue_models) + ', '

            await session.execute(update(User).where(User.id == id).values(
                dialogue_models=dialogue_models 
            ))
            await session.commit()


async def del_current_dialogue(id: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            current_dialog_index = int(user.current_dialog_index)
            dialogue_models = str(user.dialogue_models).split(', ')[0:-1]
            dialog_titles = str(user.dialog_titles).split(', ')[0:-1]

            del dialogue_models[current_dialog_index]
            del dialog_titles[current_dialog_index]

            dialogue_models = ', '.join(dialogue_models) + ', '
            dialog_titles = ', '.join(dialog_titles) + ', '

            await session.execute(update(User).where(User.id == id).values(
                dialogue_models=dialogue_models,
                dialog_titles=dialog_titles
            ))
            await session.commit()


async def set_first_promt(id: int, first_promt: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                first_promt=first_promt 
            ))
            await session.commit()


async def set_dialog_name(id: int, dialog_name: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            current_dialog_index = int(user.current_dialog_index)
            dialog_titles = str(user.dialog_titles).split(', ')[0:-1]
            dialog_titles[current_dialog_index] = dialog_name
            dialog_titles = ', '.join(dialog_titles) + ', '

            await session.execute(update(User).where(User.id == id).values(
                dialog_titles=dialog_titles 
            ))
            await session.commit()


async def set_current_dialog_index(id: int, current_dialog_index: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                current_dialog_index=current_dialog_index 
            ))
            await session.commit()


async def set_second_promt(id: int, second_promt: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                second_promt=second_promt 
            ))
            await session.commit()


async def set_default_promts(id: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                first_promt=DEFAULT_VALUES.get('first_promt'), 
                second_promt=DEFAULT_VALUES.get('second_promt'),
            ))
            await session.commit()