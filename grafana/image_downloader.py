import logging
import shutil

import requests

from configuration.settings import GrafanaSettings, PanelImageSettings

__all__ = ("GrafanaImageDownloader")

logger = logging.getLogger(__name__)


class GrafanaImageDownloader:
    def __init__(
            self,
            grafana_settings: GrafanaSettings
    ) -> None:
        self.__grafana_settings = grafana_settings

    def download(
            self,
            panel_image: PanelImageSettings,
            file_path: str
    ) -> None:
        try:
            request = requests.get(
                url=f"http://{self.__grafana_settings.host}:{self.__grafana_settings.port}/render/d-solo/"
                f"{panel_image.dashboard_uid}?from={panel_image.from_date}&to={panel_image.to_date}"
                f"&orgId={panel_image.org_id}&panelId={panel_image.panel_id}"
                f"&width={panel_image.width}&height={panel_image.height}"
                f"&tz={panel_image.tz}",
                headers={"Authorization": f"Bearer {self.__grafana_settings.api_key}"},
                stream=True
            )

            logger.info(f"Status code: {request.status_code}")
            if request.status_code == 200:
                logger.info(f"Start saving result to file: {file_path}")

                with open(file_path, 'wb') as image_file:
                    request.raw.decode_content = True
                    shutil.copyfileobj(request.raw, image_file)

        except Exception as ex:
            logger.error(f"Request exception: {repr(ex)}")

        return None
