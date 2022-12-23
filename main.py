import logging
import os
import sys
import argparse

from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
from grafana.image_downloader import GrafanaImageDownloader
from tg.telegram_service import TelegramService
from watermark.watermark_draw import WatermarkDraw

# the configuration file name
CONFIG_FILE = "settings.ini"

logger = logging.getLogger(__name__)


def prepare_logs():
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        handlers=[RotatingFileHandler('logs/downloader.log', maxBytes=100000000, backupCount=10, encoding='utf-8')],
        encoding="utf-8"
    )


if __name__ == '__main__':
    prepare_logs()

    logger.info("Program has been started")

    logger.info(f"Program arguments: {sys.argv}")
    parser = argparse.ArgumentParser()

    parser.add_argument("--dashboard", help="dashboard uid", type=str, default="")
    parser.add_argument("--panel", help="panel id", type=int, default="0")
    parser.add_argument("--f", help="from date", type=str, default="")
    parser.add_argument("--t", help="to date", type=str, default="")
    parser.add_argument("--file", help="path to file", type=str, default="")

    args = parser.parse_args()

    logger.info(f"Parsed arguments: {args}")

    try:
        config = ProgramConfiguration(
            CONFIG_FILE,
            arg_dashboard=args.dashboard,
            arg_panel=args.panel,
            arg_from=args.f,
            arg_to=args.t,
            arg_file=args.file
        )
        logger.info("Configuration has been loaded")

        logger.info(f"Grafana: {config.grafana_settings};")
        logger.info(f"Panel: {config.panel_image_settings};")
        logger.info(f"Temp storage: {config.temp_storage_settings};")
        logger.info(f"Watermark: {config.watermark_settings};")
        logger.info(f"Telegram: {config.telegram_settings}.")

        try:
            downloader = GrafanaImageDownloader(config.grafana_settings)
            logger.info("Grafana downloader has been created")

            downloader.download(config.panel_image_settings, config.temp_storage_settings.file_path)
            print(f"Image has been downloaded: {config.temp_storage_settings.file_path}")

            if config.watermark_settings.text:
                try:
                    watermark = WatermarkDraw(config.watermark_settings)
                    logger.info("Watermark has been created")

                    watermark.draw(config.temp_storage_settings.file_path)
                except Exception as ex:
                    logger.error(f"Draw watermark error has been occurred: {repr(ex)}")
                    print(f"Draw watermark error has been occurred: {repr(ex)}")
                else:
                    print(f"Watermark has been added")

            if config.telegram_settings.bot_token and config.telegram_settings.chat_id:
                try:
                    telegram = TelegramService(
                        token=config.telegram_settings.bot_token,
                        chat_id=config.telegram_settings.chat_id
                    )
                    logger.info("TelegramService has been created")

                    telegram.send_image_message(
                        image_path=config.temp_storage_settings.file_path,
                        text_description=config.telegram_settings.image_description
                    )
                except Exception as ex:
                    logger.error(f"Telegram message error has been occurred: {repr(ex)}")
                    print(f"Telegram message error has been occurred: {repr(ex)}")
                else:
                    print(f"Telegram message has been sent")

        except Exception as ex:
            logger.error(f"Download error has been occurred: {repr(ex)}")
            print(f"Download error has been occurred: {repr(ex)}")

    except Exception as ex:
        logger.error(f"Error has been occurred: {repr(ex)}")
        print(f"Error has been occurred: {repr(ex)}")

    logger.info("Program has been finished.")
