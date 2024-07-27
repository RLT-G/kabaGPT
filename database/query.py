from database.models import async_session
from database.models import User
from sqlalchemy import select, update, delete
from config import (
    DEFAULT_FIRST_PROMT, 
    DEFAULT_SECOND_PROMT, 
    DEFAULT_DIALOGUE_TITLES
)


async def create_user(id: int, chat_id: int, firstname: str = '', lastname: str = '') -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id).limit(1))

        if not user:
            session.add(User(
                id=id,
                firstname=firstname,
                lastname=lastname,
                first_promt=DEFAULT_FIRST_PROMT,
                second_promt=DEFAULT_SECOND_PROMT
            ))

            await session.commit()


async def all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
        # print(f"ID: {user.id}, Firstname: {user.firstname}, Lastname: {user.lastname}, First Prompt: {user.first_promt}, Second Prompt: {user.second_promt}")


async def set_default(id: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                first_promt=DEFAULT_FIRST_PROMT, 
                second_promt=DEFAULT_SECOND_PROMT,
                dialog_titles=DEFAULT_DIALOGUE_TITLES
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


async def set_second_promt(id: int, second_promt: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        
        if user:
            await session.execute(update(User).where(User.id == id).values(
                second_promt=second_promt 
            ))
            await session.commit()


async def set_dialogue_title(id: int, dialogue_title: str, dialogue_index: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            dialog_titles = str(user.dialog_titles).split('&#13')
            dialog_titles[dialogue_index] = dialogue_title
            dialog_for_db = "&#13".join(dialog_titles)

            await session.execute(update(User).where(User.id == id).values(
                dialog_titles=dialog_for_db 
            ))
            await session.commit()


async def set_model_to_dialogue(id: int, dialogue_index: int, model: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            dialogue_models = str(user.dialogue_models).split('&#13')
            dialogue_models[dialogue_index] = model
            dialogue_models_for_db = "&#13".join(dialogue_models)

            await session.execute(update(User).where(User.id == id).values(
                dialogue_models=dialogue_models_for_db 
            ))
            await session.commit()


async def get_button_texts(id: int, dialogue_index: int = -1):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            if dialogue_index != -1:
                return str(user.dialog_titles).split('&#13')[dialogue_index]
            
            return str(user.dialog_titles).split('&#13')
        

async def get_dialogue_models(id: int, model_index: int = -1):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            if model_index != -1:
                return str(user.dialogue_models).split('&#13')[model_index]
            
            return str(user.dialogue_models).split('&#13')
        

async def add_referral_user(referral_id: int, id: int) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == referral_id))
        user = result.scalar_one_or_none()

        if user and not id in str(user.referral_users):
            referral_users = f"{str(user.referral_users)}&#13{id}" 

            await session.execute(update(User).where(User.id == referral_id).values(
                referral_users=referral_users 
            ))
            await session.commit()


async def get_referral_count(id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            referral_users = str(user.referral_users)
            if "&#13" in referral_users:
                return len(referral_users.split('&#13')[1::])
            else:
                return 0

            str(user.referral_users).split('&#13')[model_index]
            
            return str(user.dialogue_models).split('&#13')