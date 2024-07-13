from os import path
from typing import Optional
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QMouseEvent


class Label(QLabel):
    """Custom QLabel, adds clicked signal and an index"""

    clicked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget], index: int):
        super(QLabel, self).__init__()
        self.setParent(parent)
        self.index = index

    def mousePressEvent(self, e: Optional[QMouseEvent]):
        super(QLabel, self).mousePressEvent(e)
        if e is not None:
            match e.button():
                case Qt.MouseButton.LeftButton | Qt.MouseButton.RightButton:
                    self.clicked.emit()


def get_new_path(new_path: str):
    new_path = path.dirname(path.abspath(__file__)) + new_path
    if not path.isfile(new_path):
        # temp fix for executables
        new_path = new_path.replace("/..", "")
    return new_path
