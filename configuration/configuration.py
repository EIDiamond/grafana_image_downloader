from configparser import ConfigParser

from configuration.settings import GrafanaSettings, PanelImageSettings, TempStorageSettings

__all__ = ("ProgramConfiguration")


class ProgramConfiguration:
    """
    Represent configuration
    """
    def __init__(
            self,
            configuration_file_name: str,
            arg_dashboard: str = "",
            arg_panel: int = 0,
            arg_from: str = "",
            arg_to: str = "",
            arg_file: str = ""
    ) -> None:
        # classic ini file
        config = ConfigParser(interpolation=None)
        config.read(configuration_file_name)

        self.__grafana_settings = GrafanaSettings(
            host=config["GRAFANA"]["HOST"],
            port=int(config["GRAFANA"]["PORT"]),
            api_key=config["GRAFANA"]["API_KEY"]
        )

        self.__temp_storage_settings = TempStorageSettings(
            file_path=arg_file if arg_file else config["TEMP_STORAGE"]["FILE_PATH"]
        )

        self.__panel_image_settings = PanelImageSettings(
            dashboard_uid=arg_dashboard if arg_dashboard else config["PANEL_IMAGE"]["DASHBOARD_UID"],
            panel_id=arg_panel if arg_panel else int(config["PANEL_IMAGE"]["PANEL_ID"]),
            org_id=int(config["PANEL_IMAGE"]["ORG_ID"]),
            width=int(config["PANEL_IMAGE"]["WIDTH"]),
            height=int(config["PANEL_IMAGE"]["HEIGHT"]),
            tz=config["PANEL_IMAGE"]["TZ"],
            from_date=arg_from if arg_from else config["PANEL_IMAGE"]["FROM_DATE"],
            to_date=arg_to if arg_to else config["PANEL_IMAGE"]["TO_DATE"]
        )

    @property
    def grafana_settings(self) -> GrafanaSettings:
        return self.__grafana_settings

    @property
    def temp_storage_settings(self) -> TempStorageSettings:
        return self.__temp_storage_settings

    @property
    def panel_image_settings(self) -> PanelImageSettings:
        return self.__panel_image_settings
