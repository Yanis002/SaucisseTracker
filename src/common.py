import os

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, QAbstractListModel, QObject, QRect, QSignalBlocker, QThread, Qt
from PyQt6.QtGui import QColor, QFont, QPainterPath, QPen, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import (
    QGraphicsColorizeEffect,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QMessageBox,
    QWidget,
)

if TYPE_CHECKING:
    from config import Config
    from state import LabelState, State


OS_MENU_OFFSET = 34 if os.name == "nt" else 22
GLOBAL_HALF_OPACITY = 0.58
CURRENT_XML_VERSION = (1, 0)


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


class Rotation(QThread):
    positionChanged = pyqtSignal(object)
    delta_angle = 1

    def __init__(self, config: "Config", position: int = 0):
        super().__init__()
        self.setTerminationEnabled(True)
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


class PixmapItem(QGraphicsPixmapItem):
    def __init__(
        self,
        config: "Config",
        pixmap: QPixmap,
        item_index: int,
        obj_name: str,
        default_strength: float,
        state: "LabelState",
        parent: QGraphicsItem = None,
    ):
        super().__init__(pixmap, parent)

        self.config = config
        self.item_index = item_index
        self.state = state
        self.opacity_value = GLOBAL_HALF_OPACITY if default_strength == 1.0 else 1.0
        self.setOpacity(self.opacity_value)
        self.label_counter: Optional["OutlinedGraphicsTextItem"] = None
        self.extra: Optional["PixmapItem"] = None
        self.flag: Optional["OutlinedGraphicsTextItem"] = None
        self.reward_index = 0
        self.flag_text_index = 0
        self.obj_name = obj_name
        self.is_go_mode = False
        self.is_go_mode_light = False

        # black & white effect, todo find something better? idk, enabled by default
        self.effect = QGraphicsColorizeEffect()
        self.effect.setStrength(default_strength)
        self.effect.setColor(QColor("black"))
        self.effect.setObjectName(f"{obj_name}_fx")
        self.setGraphicsEffect(self.effect)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        # do nothing if this is the go mode light
        if self.is_go_mode_light:
            return

        self.config.state_saved = False
        item = self.config.active_inv.items[self.item_index]

        if event is not None:
            match event.button():
                case Qt.MouseButton.LeftButton:
                    if self.is_go_mode:
                        self.update_gomode()
                    else:
                        self.update_item(True)
                case Qt.MouseButton.MiddleButton:
                    if not self.is_go_mode:
                        if self.flag is not None:
                            self.flag.setVisible(not self.flag.isVisible())
                        else:
                            self.update_item(True, True)
                case Qt.MouseButton.RightButton:
                    if self.is_go_mode:
                        self.update_gomode()
                    elif item.is_reward:
                        self.next_reward()
                    elif self.extra is not None:
                        self.extra.setVisible(not self.extra.isVisible())
                    else:
                        self.update_item(False)

    def wheelEvent(self, event):
        super().wheelEvent(event)

        if event is not None:
            item = self.config.active_inv.items[self.item_index]
            rewards = self.config.active_inv.rewards

            if item.use_wheel or rewards.use_wheel:
                # adapted from https://stackoverflow.com/a/20152809
                value = 0
                steps = event.delta() // 120
                for _ in range(1, abs(steps) + 1):
                    value += steps and steps // abs(steps)  # 0, 1, or -1
                    if value != 0:
                        if item.use_wheel:
                            self.update_item(value > 0, False)
                        elif rewards.use_wheel:
                            self.next_reward()

    def shape(self):
        # fixes a behavior where you need to click on the texture, which we don't want here
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def next_reward(self):
        item = self.config.active_inv.items[self.item_index]

        for i, _ in enumerate(item.positions):
            if self.obj_name.endswith(f"_pos_{i}"):
                reward = item.reward_map.get(i)

                if reward is not None and reward.item_pixmap is not None:
                    self.reward_index += 1

                    if self.reward_index > len(self.config.active_inv.rewards.items) - 1:
                        self.reward_index = 0

                    item.update_reward(i, self.config.active_inv.rewards.items[self.reward_index])

    def update_gomode(self, gomode_visibility: Optional[bool] = None):
        self.config.state_saved = False
        gomode_settings = self.config.gomode_settings
        cond = gomode_visibility if gomode_visibility is not None else self.effect.strength() > 0.0

        if self.effect is not None:
            if cond:
                self.effect.setStrength(0.0)
                self.setOpacity(1.0)
            else:
                self.effect.setStrength(1.0)
                self.setOpacity(0.001 if gomode_settings.hide_if_disabled else GLOBAL_HALF_OPACITY)

        if gomode_visibility is None:
            self.config.label_gomode_light.setVisible(not self.config.label_gomode_light.isVisible())

    def update_item(self, increase: bool, middle_click: bool = False):
        item = self.config.active_inv.items[self.item_index]
        path_index = 0

        if not middle_click and len(item.paths) > 1:
            if increase:
                self.state.infos.img_index += 1
                self.flag_text_index += 1
            else:
                self.state.infos.img_index -= 1
                self.flag_text_index -= 1

            if self.flag is not None and item.flag_index is not None:
                flag = self.config.flags[item.flag_index]
                total = len(flag.texts) - 1

                if self.flag_text_index > total:
                    self.flag_text_index = 0
                if self.flag_text_index < 0:
                    self.flag_text_index = total

                self.flag.setPlainText(flag.texts[self.flag_text_index])
                self.flag.set_text_style(flag.text_settings_index, self.flag_text_index == total)

            if self.state.infos.img_index > len(item.paths) - 1:
                self.state.infos.img_index = -1
            if self.state.infos.img_index < -1:
                self.state.infos.img_index = len(item.paths) - 1

            if self.state.infos.img_index < 0:
                self.effect.setStrength(1.0)  # enable filter
                self.setOpacity(GLOBAL_HALF_OPACITY)
                path_index = 0
            else:
                self.effect.setStrength(0.0)  # disable filter
                self.setOpacity(1.0)
                path_index = self.state.infos.img_index

            self.setPixmap(QPixmap(str(item.paths[path_index])))

            if self.state.infos.img_index < 0:
                self.setOpacity(GLOBAL_HALF_OPACITY)
            else:
                self.setOpacity(1.0)
        elif self.label_counter is not None and item.counter is not None:
            if increase:
                item.counter.incr(middle_click)
            else:
                item.counter.decr()

            if self.effect is not None:
                item.counter.update(self)
        else:
            if self.effect.strength() > 0.0:
                self.effect.setStrength(0.0)
                self.setOpacity(1.0)
            else:
                self.effect.setStrength(1.0)
                self.setOpacity(GLOBAL_HALF_OPACITY)


# from https://stackoverflow.com/a/78362730
class OutlinedGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, config: "Config", parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)

        self.config = config
        self.outline_size = 0.0
        self.format = QTextCharFormat()
        self.item_pixmap: Optional[PixmapItem] = None

        self.outlineFormat = QTextCharFormat()
        self.dummyFormat = QTextCharFormat()
        self.dummyFormat.setTextOutline(QPen(Qt.GlobalColor.transparent))

        children = self.findChildren(QObject)
        if not children:
            super().setPlainText("")
            children = self.findChildren(QObject)
        if self.toPlainText():
            # ensure we call our version of setPlainText()
            self.setPlainText(self.toPlainText())

        for obj in children:
            if obj.metaObject().className() == "QWidgetTextControl":
                self.textControl = obj
                break

    @staticmethod
    def new(
        config: "Config",
        obj_name: str,
        geometry: QRect,
        text: str,
        text_settings_index: int,
        rotation: int,
        parent: Optional[QGraphicsItem] = None,
    ):
        new_item = OutlinedGraphicsTextItem(config, parent)
        new_item.setPos(geometry.x(), geometry.y())
        new_item.setPlainText(text)
        new_item.set_text_style(text_settings_index, False)
        new_item.setObjectName(obj_name)
        new_item.setRotation(float(rotation))
        return new_item

    def setPlainText(self, text):
        super().setPlainText(text)

        if len(text) > 0:
            self.update_format(self.format.font(), self.format.foreground())

    def paint(self, painter, option, widget):
        with QSignalBlocker(self.textControl):
            cursor = QTextCursor(self.document())
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.mergeCharFormat(self.outlineFormat)
            super().paint(painter, option, widget)
            cursor.mergeCharFormat(self.dummyFormat)
            super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event is not None and self.item_pixmap is not None:
            match event.button():
                case Qt.MouseButton.LeftButton:
                    self.item_pixmap.update_item(True)
                case Qt.MouseButton.MiddleButton:
                    self.item_pixmap.update_item(True, True)
                case Qt.MouseButton.RightButton:
                    self.item_pixmap.update_item(False)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print("new pos:", self.pos())

    def wheelEvent(self, event):
        super().wheelEvent(event)

        if event is not None:
            item = self.config.active_inv.items[self.item_pixmap.item_index]
            rewards = self.config.active_inv.rewards

            if item.use_wheel or rewards.use_wheel:
                # adapted from https://stackoverflow.com/a/20152809
                value = 0
                steps = event.delta() // 120
                for _ in range(1, abs(steps) + 1):
                    value += steps and steps // abs(steps)  # 0, 1, or -1
                    if value != 0:
                        if item.use_wheel:
                            self.item_pixmap.update_item(value > 0, False)
                        elif rewards.use_wheel:
                            # does nothing for now
                            pass

    def update_format(self, font: QFont, color: QColor):
        self.outlineFormat.setTextOutline(
            QPen(
                Qt.GlobalColor.black,
                self.outline_size,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )

        self.format.setFont(font)
        self.format.setForeground(color)
        cursor = QTextCursor(self.document())
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeCharFormat(self.format)

    def set_text_style(self, text_settings_index: int, is_max: bool):
        text_settings = self.config.get_text_settings(text_settings_index)
        font = self.config.get_font(text_settings)
        color = self.config.get_color(text_settings, is_max)
        self.outline_size = text_settings.outline_thickness * 2
        self.update_format(
            QFont(font.name, int(text_settings.size), 75 if text_settings.bold else 1), Color.convert(color)
        )


class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def unpack(value: int):
        return Color((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)

    @staticmethod
    def pack(color: "Color"):
        return ((color.r & 0xFF) << 16) | ((color.g & 0xFF) << 8) | (color.b & 0xFF)

    @staticmethod
    def convert(color: "Color"):
        return QColor(color.r, color.g, color.b)


@dataclass
class Pos:
    x: int
    y: int

    def to_str(self):
        return f"{self.x};{self.y}"


def show_message(parent: QWidget, title: str, icon: QMessageBox.Icon, text: str):
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setIcon(icon)
    message_box.setText(text)
    message_box.show()


def show_error(parent: QWidget, text: str):
    show_message(parent, "Error", QMessageBox.Icon.Critical, text)


def show_info(parent: QWidget, text: str):
    show_message(parent, "Info", QMessageBox.Icon.Information, text)
