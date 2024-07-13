import sys

from os import getcwd, path
from typing import Optional
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QMouseEvent


class Label(QLabel):
    """Custom QLabel, adds clicked signals and an index to identify easily which inventory item it is"""

    clicked = pyqtSignal()
    clicked_left = pyqtSignal()
    clicked_middle = pyqtSignal()
    clicked_right = pyqtSignal()

    def __init__(self, parent: Optional[QWidget], index: int):
        super(QLabel, self).__init__()

        self.setParent(parent)
        self.index = index
        self.img_index = -1
        self.tier_index = -1

    def mousePressEvent(self, e: Optional[QMouseEvent]):
        super(QLabel, self).mousePressEvent(e)

        if e is not None:
            match e.button():
                case Qt.MouseButton.LeftButton | Qt.MouseButton.MiddleButton | Qt.MouseButton.RightButton:
                    self.clicked.emit()

                    if e.button() == Qt.MouseButton.LeftButton:
                        self.clicked_left.emit()
                    elif e.button() == Qt.MouseButton.MiddleButton:
                        self.clicked_middle.emit()
                    else:
                        self.clicked_right.emit()


# adapted from https://stackoverflow.com/a/42615559
def get_app_path():
    if getattr(sys, 'frozen', False):
        return getcwd()
    elif __file__:
        return path.dirname(path.abspath(__file__)).removesuffix("src")
    else:
        raise RuntimeError("ERROR: couldn't determine the execution type")


def get_new_path(new_path: str, is_bundled: bool = False):
    if is_bundled:
        new_path = path.join(path.dirname(path.abspath(__file__)).removesuffix("src"), new_path) 
    else: 
        new_path = path.join(get_app_path(), new_path)

    if not path.isfile(new_path):
        raise RuntimeError(f"ERROR: invalid path: '{new_path}'")

    return new_path


def unpack_color(color: int):
    return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF
