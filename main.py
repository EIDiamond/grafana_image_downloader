import logging
import os
import sys
import argparse

from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
from grafana.image_downloader import GrafanaImageDownloader

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

        logger.info(f"Grafana: {config.grafana_settings};"
                    f" Panel: {config.panel_image_settings};"
                    f" temp storage: {config.temp_storage_settings}")

        downloader = GrafanaImageDownloader(config.grafana_settings)
        logger.info("Grafana downloader has been created")
        
        try:
            logger.info(f"Download image to: {config.temp_storage_settings.file_path}")

            downloader.download(config.panel_image_settings, config.temp_storage_settings.file_path)
        except Exception as ex:
            logger.error(f"Download error has been occurred: {repr(ex)}")

    except Exception as ex:
        logger.error(f"Error has been occurred: {repr(ex)}")

    logger.info("Program has been finished.")
