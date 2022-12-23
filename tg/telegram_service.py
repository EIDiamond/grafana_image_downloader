import logging

import telegram

__all__ = ("TelegramService")

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, token: str, chat_id: str) -> None:
        self.__bot = telegram.Bot(token=token)
        self.__chat_id = chat_id

    def send_text_message(self, text: str):
        logger.debug(f"Telegram: send  message {text}")
        self.__bot.sendMessage(chat_id=self.__chat_id, text=text)

    def send_image_message(self, image_path: str, text_description: str = ""):
        logger.debug(f"Telegram: send image: {image_path} with description {text_description}")
        self.__bot.send_photo(
            chat_id=self.__chat_id,
            photo=open(image_path, 'rb'),
            caption=text_description
        )
