from sqlalchemy import BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///database/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'Users'

    id = mapped_column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(128), unique=False, nullable=True)
    lastname: Mapped[str] = mapped_column(String(128), unique=False, nullable=True)
    first_promt: Mapped[str] = mapped_column(Text(2048), unique=False)
    second_promt: Mapped[str] = mapped_column(Text(2048), unique=False)
    referral_users: Mapped[str] = mapped_column(String(2048), nullable=True, default='')
    dialog_titles: Mapped[str] = mapped_column(String(1024), default='Диалог 1&#13Диалог 2&#13Диалог 3&#13Диалог 4&#13Диалог 5')
    dialogue_models: Mapped[str] = mapped_column(String(512), default='gpt-4o-mini&#13gpt-4o-mini&#13gpt-4o-mini&#13gpt-4o-mini&#13gpt-4o-mini')
    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
