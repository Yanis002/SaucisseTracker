import math

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, Qt, QSize, QPoint, QRect, QAbstractListModel, QThread
from PyQt6.QtWidgets import QLabel, QWidget, QGraphicsColorizeEffect, QMessageBox
from PyQt6.QtGui import (
    QMouseEvent,
    QPixmap,
    QPainter,
    QPainterPath,
    QBrush,
    QPen,
    QFontMetrics,
    QColor,
    QWheelEvent,
    QTransform,
)

if TYPE_CHECKING:
    from config import Config
    from state import State


GLOBAL_HALF_OPACITY = 0.6


class ListViewModel(QAbstractListModel):
    def __init__(self, items: list[tuple[bool, str, Path]]):
        super(ListViewModel, self).__init__()
        self.items = items

    def data(self, index, role):
        status, text, img = self.items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return text

        if role == Qt.ItemDataRole.DecorationRole:
            if status:
                return img

    def rowCount(self, index):
        return len(self.items)


# from https://stackoverflow.com/a/64291055
class OutlinedLabel(QLabel):
    clicked = pyqtSignal()
    clicked_left = pyqtSignal()
    clicked_middle = pyqtSignal()
    clicked_right = pyqtSignal()

    def __init__(self, config: "Config", parent: Optional[QWidget]):
        super().__init__()
        self.w = 1 / 25
        self.mode = True
        self.setBrush(Qt.GlobalColor.white)
        self.setPen(Qt.GlobalColor.black)
        self.setParent(parent)
        self.config = config

        self.reward_index = 0
        self.item_label: Optional["Label"] = None

    @staticmethod
    def new(
        parent: "Label",
        config: "Config",
        obj_name: str,
        geometry: QRect,
        text: str,
        text_settings_index: int,
    ):
        new_label = OutlinedLabel(config, parent)
        new_label.setObjectName(obj_name)
        new_label.setGeometry(geometry)
        new_label.setText(text)
        new_label.set_text_style(text_settings_index, False)
        new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return new_label

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

    def wheelEvent(self, e: Optional[QWheelEvent]):
        super(QLabel, self).wheelEvent(e)

        if e is not None:
            item = self.config.active_inv.items[self.item_label.index]
            if item.use_wheel:
                # adapted from https://stackoverflow.com/a/20152809
                value = 0
                steps = e.angleDelta().y() // 120
                for _ in range(1, abs(steps) + 1):
                    value += steps and steps // abs(steps)  # 0, 1, or -1
                    if value != 0:
                        self.item_label.update_label(value > 0, False)

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

    def set_text_style(self, text_settings_index: int, is_max: bool):
        text_settings = self.config.get_text_settings(text_settings_index)
        font = self.config.get_font(text_settings)
        color = self.config.get_color(text_settings, is_max)

        self.setScaledOutlineMode(False)
        self.setOutlineThickness(text_settings.outline_thickness)
        self.setBrush(QColor(color.r, color.g, color.b))
        self.setStyleSheet(
            f"""
                font: {'75' if text_settings.bold else ''} {text_settings.size}pt "{font.name}";
                color: rgb({color.r}, {color.g}, {color.b});
            """
        )


class Label(QLabel):
    """Custom QLabel, adds clicked signals and an index to identify easily which inventory item it is"""

    clicked = pyqtSignal()
    clicked_left = pyqtSignal()
    clicked_middle = pyqtSignal()
    clicked_right = pyqtSignal()

    def __init__(self, config: "Config", state: "State", parent: Optional[QWidget], index: int, name: str):
        super(QLabel, self).__init__()

        self.config = config
        self.state = state
        self.setParent(parent)
        self.index = index
        self.name = name

        self.flag_text_index = 0
        self.reward_index = 0
        self.original_pixmap: Optional[QPixmap] = None
        self.label_counter: Optional[OutlinedLabel] = None
        self.label_effect: Optional[QGraphicsColorizeEffect] = None
        self.label_flag: Optional[OutlinedLabel] = None
        self.label_extra_img: Optional["Label"] = None

    @staticmethod
    def new(
        config: "Config",
        state: "State",
        parent: QWidget,
        index: int,
        name: str,
        obj_name: str,
        geometry: QRect,
        img_path: str,
        opacity: float,
        scale_content: bool,
        default_strength: float,
    ):
        new_label = Label(config, state, parent, index, name)
        new_label.setObjectName(obj_name)
        new_label.setGeometry(geometry)
        new_label.setText("")
        new_label.original_pixmap = QPixmap(img_path)
        new_label.setPixmap(new_label.original_pixmap)
        new_label.set_pixmap_opacity(opacity)
        new_label.setScaledContents(scale_content)
        new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # black & white effect, todo find something better? idk, enabled by default
        new_label_effect = QGraphicsColorizeEffect(new_label)
        new_label_effect.setStrength(default_strength)
        new_label_effect.setColor(QColor("black"))
        new_label_effect.setObjectName(f"{obj_name}_fx")
        new_label.setGraphicsEffect(new_label_effect)
        new_label.label_effect = new_label_effect

        return new_label

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

    def wheelEvent(self, e: Optional[QWheelEvent]):
        super(QLabel, self).wheelEvent(e)

        if e is not None:
            item = self.config.active_inv.items[self.index]
            if item.use_wheel:
                # adapted from https://stackoverflow.com/a/20152809
                value = 0
                steps = e.angleDelta().y() // 120
                for _ in range(1, abs(steps) + 1):
                    value += steps and steps // abs(steps)  # 0, 1, or -1
                    if value != 0:
                        self.update_label(value > 0, False)

    def set_pixmap_opacity(self, opacity: float):
        pixmap = self.pixmap().copy()
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(QPoint(), self.pixmap())
        painter.end()
        self.setPixmap(pixmap)

    def update_gomode(self, gomode_visibility: Optional[bool] = None):
        self.config.state_saved = False
        gomode_settings = self.config.gomode_settings
        cond = gomode_visibility if gomode_visibility is not None else self.label_effect.strength() > 0.0

        if self.label_effect is not None:
            if cond:
                self.label_effect.setStrength(0.0)
                self.setPixmap(self.original_pixmap)
            else:
                self.label_effect.setStrength(1.0)
                self.set_pixmap_opacity(0.0 if gomode_settings.hide_if_disabled else GLOBAL_HALF_OPACITY)

        if gomode_visibility is None:
            self.config.label_gomode_light.setVisible(not self.config.label_gomode_light.isVisible())

    def update_label(self, increase: bool, middle_click: bool = False):
        if self.label_effect is not None:
            item = self.config.active_inv.items[self.index]
            path_index = 0

            lbl_state = self.state.get_label_state_from_index(self.index)

            if lbl_state is None:
                show_error(self, "ERROR: the label state can't be found!")
                return

            if not middle_click and len(item.paths) > 1:
                if increase:
                    lbl_state.infos.img_index += 1
                    self.flag_text_index += 1
                else:
                    lbl_state.infos.img_index -= 1
                    self.flag_text_index -= 1

                if self.label_flag is not None and item.flag_index is not None:
                    flag = self.config.flags[item.flag_index]
                    total = len(flag.texts) - 1

                    if self.flag_text_index > total:
                        self.flag_text_index = 0
                    if self.flag_text_index < 0:
                        self.flag_text_index = total

                    self.label_flag.setText(flag.texts[self.flag_text_index])
                    self.label_flag.set_text_style(flag.text_settings_index, self.flag_text_index == total)

                if lbl_state.infos.img_index > len(item.paths) - 1:
                    lbl_state.infos.img_index = -1
                if lbl_state.infos.img_index < -1:
                    lbl_state.infos.img_index = len(item.paths) - 1

                if lbl_state.infos.img_index < 0:
                    self.label_effect.setStrength(1.0)  # enable filter
                    self.set_pixmap_opacity(GLOBAL_HALF_OPACITY)
                    path_index = 0
                else:
                    self.label_effect.setStrength(0.0)  # disable filter
                    self.setPixmap(self.original_pixmap)
                    path_index = lbl_state.infos.img_index

                self.original_pixmap = QPixmap(str(item.paths[path_index]))
                self.setPixmap(self.original_pixmap)

                if lbl_state.infos.img_index < 0:
                    self.set_pixmap_opacity(GLOBAL_HALF_OPACITY)
                else:
                    self.setPixmap(self.original_pixmap)
            elif self.label_counter is not None:
                if increase:
                    item.counter.incr(middle_click)
                else:
                    item.counter.decr()

                if self.label_effect is not None:
                    item.counter.update(self)
            else:
                if self.label_effect is not None:
                    if self.label_effect.strength() > 0.0:
                        self.label_effect.setStrength(0.0)
                        self.setPixmap(self.original_pixmap)
                    else:
                        self.label_effect.setStrength(1.0)
                        self.set_pixmap_opacity(GLOBAL_HALF_OPACITY)


# from https://stackoverflow.com/a/74249310
class RotationWidget(QWidget):
    position = 0
    rotation = 0

    def __init__(self, image):
        super().__init__()
        self.image = QPixmap(image)
        self.setFixedSize(self.image.size())
        self.transform = QTransform()
        half = self.image.size() / 2
        self.tX = half.width()
        self.tY = half.height()

    @staticmethod
    def new(
        parent: QWidget,
        obj_name: str,
        geometry: QRect,
        img_path: str,
    ):
        new_label = RotationWidget(img_path)
        new_label.setObjectName(obj_name)
        new_label.setGeometry(geometry)
        new_label.setParent(parent)

        return new_label

    def setPosition(self, pos):
        if self.position != pos:
            self.rotation = pos - self.position
        else:
            self.rotation = 0
        self.position = pos
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.transform.translate(self.tX, self.tY)
        self.transform.rotate(self.rotation)
        self.transform.translate(-self.tX, -self.tY)
        qp.setTransform(self.transform)
        qp.drawPixmap(0, 0, self.image)
        qp.end()


class Rotation(QThread):
    positionChanged = pyqtSignal(object)
    delta_angle = 1

    def __init__(self, config: "Config", position: int = 0):
        super().__init__()
        self.config = config
        self.position = position
        self.speed = self.config.gomode_settings.rotation_speed
        self.thread_refresh = self.config.gomode_settings.thread_refresh_rate

    def run(self):
        while True:
            diff = self.thread_refresh * self.speed
            self.position = round((self.position + diff) % 360, 2)
            self.positionChanged.emit(self.position)
            self.msleep(int(self.thread_refresh * 1000))


def show_message(parent: QWidget, title: str, icon: QMessageBox.Icon, text: str):
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setIcon(icon)
    message_box.setText(text)
    message_box.show()


def show_error(parent: QWidget, text: str):
    show_message(parent, "Error", QMessageBox.Icon.Critical, text)
