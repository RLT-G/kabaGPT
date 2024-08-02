from sqlalchemy import BigInteger, String, ForeignKey, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///data/database/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'Users'

    id = mapped_column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(128), unique=False, nullable=True)
    lastname: Mapped[str] = mapped_column(String(128), unique=False, nullable=True)

    balance: Mapped[str] = mapped_column(String(1024), default='0.0')
    referral_balance: Mapped[str] = mapped_column(String(1024), default='0.0')
    last_invoice: Mapped[str] = mapped_column(String(1024), default='0.0')


    first_promt: Mapped[str] = mapped_column(Text(2048), unique=False)
    second_promt: Mapped[str] = mapped_column(Text(2048), unique=False)

    referral_user: Mapped[str] = mapped_column(BigInteger, unique=False, nullable=True, default=0)
    referral_count: Mapped[str] = mapped_column(Integer(), default=0)

    dialog_titles: Mapped[str] = mapped_column(String(1024), default='1. ChatGPT-4o-mini, ')
    dialogue_models: Mapped[str] = mapped_column(String(512), default='gpt-4o-mini, ')

    current_dialog_index: Mapped[int] = mapped_column(Integer(), nullable=True, default=None)
    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
