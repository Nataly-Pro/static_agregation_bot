import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TgBot:
    # Токен для доступа к телеграм-боту
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    return Config(tg_bot=TgBot(token=os.getenv('BOT_TOKEN')))


config = load_config('../.env')
bot_token = config.tg_bot.token

