import logging

from PIL import Image, ImageDraw, ImageFont

from configuration.settings import WatermarkSettings

__all__ = ("WatermarkDraw")

logger = logging.getLogger(__name__)


class WatermarkDraw:
    def __init__(
            self,
            watermark_settings: WatermarkSettings
    ) -> None:
        self.__watermark_settings = watermark_settings

    def draw(
            self,
            image_path: str
    ) -> None:
        logger.info(f"Start draw watermark on image: {image_path}")

        original_image = Image.open(image_path)
        width, height = original_image.size
        logger.debug(f"Image size width: {width}; height: {height}")

        draw = ImageDraw.Draw(original_image)

        font = ImageFont.truetype(self.__watermark_settings.font, self.__watermark_settings.font_size)
        text_width, text_height = draw.textsize(self.__watermark_settings.text, font)
        logger.debug(f"Text size width: {text_width}; height: {text_height}")

        # calculate coordinates
        x = width - text_width - self.__watermark_settings.margin
        y = height - text_height - self.__watermark_settings.margin
        logger.debug(f"Text coordinates: {x}; height: {y}")

        draw.text((x, y), self.__watermark_settings.text, font=font)

        logger.info(f"Save image with watermark: {image_path}")
        original_image.save(image_path)
