import sys
import math

from os import getcwd, path
from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, Qt, QSize, QPoint
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPainterPath, QBrush, QPen, QFontMetrics, QColor

if TYPE_CHECKING:
    from config import Config, TextSettings, InventoryItem


# from https://stackoverflow.com/a/64291055
class OutlinedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = 1 / 25
        self.mode = True
        self.setBrush(Qt.GlobalColor.white)
        self.setPen(Qt.GlobalColor.black)

    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state

    def outlineThickness(self):
        return self.w * self.font().pointSize() if self.mode else self.w

    def setOutlineThickness(self, value):
        self.w = value

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            pen = QPen(pen)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.pen = pen

    def sizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().sizeHint() + QSize(w, w)

    def minimumSizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().minimumSizeHint() + QSize(w, w)

    def paintEvent(self, event):
        if self.text() == "":
            return
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        tr = metrics.boundingRect(self.text()).adjusted(0, 0, int(w), int(w))
        if self.indent() == -1:
            if self.frameWidth():
                indent = (metrics.boundingRect("x").width() + w * 2) / 2
            else:
                indent = w
        else:
            indent = self.indent()

        if self.alignment() & Qt.AlignmentFlag.AlignLeft:
            x = rect.left() + indent - min(metrics.leftBearing(self.text()[0]), 0)
        elif self.alignment() & Qt.AlignmentFlag.AlignRight:
            x = rect.x() + rect.width() - indent - tr.width()
        else:
            x = (rect.width() - tr.width()) / 2

        if self.alignment() & Qt.AlignmentFlag.AlignTop:
            y = rect.top() + indent + metrics.ascent()
        elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
            y = rect.y() + rect.height() - indent - metrics.descent()
        else:
            y = (rect.height() + metrics.ascent() - metrics.descent()) / 2

        path = QPainterPath()
        path.addText(x, y, self.font(), self.text())
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.pen.setWidthF(w * 2)
        qp.strokePath(path, self.pen)
        if 1 < self.brush.style().value < 15:
            qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)

    def set_counter_style(self, config: "Config", counter_settings: "TextSettings", is_max: bool):
        font = config.fonts[counter_settings.font]
        color = counter_settings.color_max if is_max else counter_settings.color

        self.setScaledOutlineMode(False)
        self.setOutlineThickness(2)
        self.setBrush(QColor(color.r, color.g, color.b))
        self.setStyleSheet(
            f"""
                font: {'75' if counter_settings.bold else ''} {counter_settings.size}pt "{font.name}";
                color: rgb({color.r}, {color.g}, {color.b});
            """
        )


class Label(QLabel):
    """Custom QLabel, adds clicked signals and an index to identify easily which inventory item it is"""

    clicked = pyqtSignal()
    clicked_left = pyqtSignal()
    clicked_middle = pyqtSignal()
    clicked_right = pyqtSignal()

    def __init__(self, parent: Optional[QWidget], index: int, name: str):
        super(QLabel, self).__init__()

        self.setParent(parent)
        self.index = index
        self.name = name
        self.img_index = -1
        self.original_pixmap: Optional[QPixmap] = None

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

    def set_pixmap_opacity(self, opacity: float):
        pixmap = self.pixmap().copy()
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(QPoint(), self.pixmap())
        painter.end()
        self.setPixmap(pixmap)

    def update_label(self, config: "Config", item: "InventoryItem", increase: bool):
        label_effect = None

        for i, _ in enumerate(item.positions):
            label_effect = config.active_inv.label_effect_map[self.index][i]
            if self.objectName() in label_effect.objectName():
                break
            else:
                label_effect = None

        if label_effect is not None:
            path_index = 0

            label_counter_map = config.active_inv.label_counter_map.get(self.index)
            if label_counter_map is not None:
                label_counter = label_counter_map.get(i)
            else:
                label_counter = None

            if len(item.paths) > 1:
                if increase:
                    self.img_index += 1
                else:
                    self.img_index -= 1

                if self.img_index > len(item.paths) - 1:
                    self.img_index = -1
                if self.img_index < -1:
                    self.img_index = len(item.paths) - 1

                if self.img_index < 0:
                    label_effect.setStrength(1.0)  # enable filter
                    self.set_pixmap_opacity(0.75)
                    path_index = 0
                else:
                    label_effect.setStrength(0.0)  # disable filter
                    self.setPixmap(self.original_pixmap)
                    path_index = self.img_index

                self.original_pixmap = QPixmap(get_new_path(f"config/oot/{item.paths[path_index]}"))
                self.setPixmap(self.original_pixmap)

                if self.img_index < 0:
                    self.set_pixmap_opacity(0.75)
                else:
                    self.setPixmap(self.original_pixmap)
            elif label_counter is not None:
                if increase:
                    item.counter.incr()
                else:
                    item.counter.decr()

                if item.counter.show:
                    counter_settings = config.text_settings[item.counter.text_settings_index]
                    label_effect.setStrength(0.0)  # disable filter
                    self.setPixmap(self.original_pixmap)
                    label_counter.setText(f"{item.counter.value}")
                    label_counter.set_counter_style(config, counter_settings, item.counter.value == item.counter.max)
                else:
                    label_effect.setStrength(1.0)  # enable filter
                    self.set_pixmap_opacity(0.75)
                    label_counter.setText("")
            else:
                if label_effect.strength() > 0.0:
                    label_effect.setStrength(0.0)
                    self.setPixmap(self.original_pixmap)
                else:
                    label_effect.setStrength(1.0)
                    self.set_pixmap_opacity(0.75)


# adapted from https://stackoverflow.com/a/42615559
def get_app_path():
    if getattr(sys, "frozen", False):
        return getcwd()
    elif __file__:
        return path.dirname(path.abspath(__file__)).removesuffix("src")
    else:
        raise RuntimeError("ERROR: couldn't determine the execution type")


def get_new_path(new_path: str, is_bundled: bool = False, check_exists: bool = True):
    if is_bundled:
        new_path = path.join(path.dirname(path.abspath(__file__)).removesuffix("src"), new_path)
    else:
        new_path = path.join(get_app_path(), new_path)

    if check_exists and not path.isfile(new_path):
        raise RuntimeError(f"ERROR: invalid path: '{new_path}'")

    return new_path
