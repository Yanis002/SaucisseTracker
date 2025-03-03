import tracker

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QWidget

from config import Config


class TrackerEditor(tracker.TrackerWindow):
    def __init__(self, parent: Optional[QWidget], configs: dict[Path, Config], config_index: int):
        super().__init__(parent, configs, config_index, True)
