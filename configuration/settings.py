from dataclasses import dataclass

__all__ = ("GrafanaSettings", "PanelImageSettings", "TempStorageSettings", "WatermarkSettings")


@dataclass(eq=False, repr=True)
class GrafanaSettings:
    host: str
    port: int
    api_key:  str


@dataclass(eq=False, repr=True)
class PanelImageSettings:
    dashboard_uid: str
    panel_id: int
    org_id: int
    width: int
    height: int
    tz: str
    from_date: str
    to_date: str


@dataclass(eq=False, repr=True)
class TempStorageSettings:
    file_path: str


@dataclass(eq=False, repr=True)
class WatermarkSettings:
    text: str
    font: str
    font_size: int
    margin: int
