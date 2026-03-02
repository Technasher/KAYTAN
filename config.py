from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Optional

CONFIG = dotenv_values()

# class Settings(BaseSettings):
#
#     # Сообщаем Pydantic, что нужно загрузить .env файл
#     model_config = SettingsConfigDict(
#         env_file='.env',  # Какой файл загружать
#         env_file_encoding='utf-8',
#         case_sensitive=False  # Имена переменных не чувствительны к регистру
#     )
#     DB_URL: str
#
# # Создаем единственный экземпляр настроек для всего приложения
# settings = Settings()
