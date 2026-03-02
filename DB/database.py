import os
from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from DB.models.base import Base
from config import CONFIG

engine = create_async_engine(CONFIG['DB_URL'])
session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    async with engine.begin() as conn:
        # Здесь важно, чтобы все модели были уже импортированы
        await conn.run_sync(Base.metadata.create_all)

# Функция-генератор для FastAPI/Depends
# def get_db():
#     session = session()
#     try:
#         yield session
#     finally:
#         session.close()
