import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / '.env')


@dataclass
class TgBot:
    # Токен для доступа к телеграм-боту
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    return Config(tg_bot=TgBot(token=os.getenv('BOT_TOKEN')))


