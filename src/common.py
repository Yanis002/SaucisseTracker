import os

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile
from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, QAbstractListModel, QObject, QRect, QSignalBlocker, QThread, Qt
from PyQt6.QtGui import QColor, QGuiApplication, QFont, QPainterPath, QPen, QPixmap, QTextCharFormat, QTextCursor
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
CURRENT_STATE_VERSION = (1, 0)
DEBUG_PRINTS = False


class ListViewModel(QAbstractListModel):
    """Widget that handles a list where each entry can have both a name and an image."""

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
    """Thread used to update the rotation value of the go-mode light effect."""

    # signal to use to get the value since you can't do that directly from the `run` function
    positionChanged = pyqtSignal(object)

    def __init__(self, config: "Config", position: int = 0):
        super().__init__()
        self.setTerminationEnabled(True)
        self.config = config
        self.position = position
        self.speed = self.config.gomode_settings.rotation_speed
        self.thread_refresh = self.config.gomode_settings.thread_refresh_rate
        self.do_run = True
        self.pause_update = False
        self.setObjectName("RotationThread")

    def stop(self):
        self.do_run = False
        self.quit()
        self.wait()

    def run(self):
        while self.do_run:
            if self.pause_update:
                continue

            if self.config.label_gomode_light is not None and self.config.label_gomode_light.isVisible():
                diff = self.thread_refresh * self.speed
                self.position = round((self.position + diff) % 360, 2)
                self.positionChanged.emit(self.position)
            self.msleep(int(self.thread_refresh * 1000))


class PixmapItem(QGraphicsPixmapItem):
    """
    Widget used to add more functionnalities to `QGraphicsPixmapItem`.
    It's handling item updates (from user actions or when loading a savestate).
    """

    def __init__(
        self,
        config: "Config",
        pixmap: QPixmap,
        item_index: int,
        obj_name: str,
        default_strength: float,
        state: "LabelState",
        parent: QGraphicsItem = None,
        create_effect: bool = True,
    ):
        super().__init__(pixmap, parent)

        self.config = config
        self.state = state
        self.opacity_value = GLOBAL_HALF_OPACITY if default_strength == 1.0 else 1.0
        self.setOpacity(self.opacity_value)
        self.label_counter: Optional["OutlinedGraphicsTextItem"] = None
        self.extra: Optional["PixmapItem"] = None
        self.flag: Optional["OutlinedGraphicsTextItem"] = None
        self.obj_name = obj_name
        self.initial_scale = self.scale()

        # used for the black & white effect, enabled by default
        if create_effect:
            self.effect = QGraphicsColorizeEffect()
            self.effect.setStrength(default_strength)
            self.effect.setColor(QColor("black"))
            self.effect.setObjectName(f"{obj_name}_fx")
            self.setGraphicsEffect(self.effect)
        else:
            self.effect = None

    def mousePressEvent(self, event):
        """Actions to do when there's a click (left, right or middle). This is the entrypoint of updating items."""

        # editor only, avoid updating the item if it can be moved
        if self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            super().mousePressEvent(event)
            return

        # we need to call the original function in order to get updates through go-mode light working
        # but as a side-effect flags are harder to disable on rewards, so we simply ignore this call if it's a flag
        if self.flag is None:
            super().mousePressEvent(event)

        # do nothing if this is the go mode light
        if self.state.is_gomode_light:
            return

        item = self.config.active_inv.items[self.state.index]

        if event is not None:
            match event.button():
                case Qt.MouseButton.LeftButton:
                    # left clicks are used to enable the go-mode thing (takes the priority) and the other items from the tracker
                    if self.state.is_gomode:
                        self.update_gomode()
                    else:
                        self.update_item(True)
                    self.config.state_saved = False
                case Qt.MouseButton.MiddleButton:
                    # middle clicks are used to enable flags on the rewards, it can also be used to update items but it will do
                    # special actions like incrementing by N a counter (if the feature is used, as set by the config file)
                    if not self.state.is_gomode:
                        if self.flag is not None:
                            self.flag.setVisible(not self.flag.isVisible())
                            self.state.infos.show_flag = self.flag.isVisible()
                        else:
                            self.update_item(True, True)
                        self.config.state_saved = False
                case Qt.MouseButton.RightButton:
                    # right clicks can also show or hide the go-mode thing, it's also used to update rewards and the extra stuff
                    # used for the songs for OoT (for example), also it can updates other items like the other clicks
                    if self.state.is_gomode:
                        self.update_gomode()
                    elif item.is_reward:
                        self.next_reward(True)
                    elif self.extra is not None and item.extra_index is not None:
                        self.extra.setVisible(not self.extra.isVisible())
                        self.state.infos.show_extra_img = self.extra.isVisible()
                    else:
                        self.update_item(False)
                    self.config.state_saved = False

    def mouseReleaseEvent(self, event):
        """Actions to do when the mouse is released, updates the position on the editor"""

        super().mouseReleaseEvent(event)

        if self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if self.config.edit_menu is not None:
                self.config.edit_menu.update_pos(self.pos().toPoint())

    def mouseMoveEvent(self, event):
        """Actions to do when the mouse is moving, updates the position on the editor"""

        super().mouseMoveEvent(event)

        if self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if self.config.edit_menu is not None:
                self.config.edit_menu.update_pos(self.pos().toPoint())

    def wheelEvent(self, event):
        """Actions to do when the wheel is 'moved'. Used as a fast-cycle feature when enabled in the config."""

        super().wheelEvent(event)

        if self.is_gomode():
            return

        if event is not None:
            item = self.config.active_inv.items[self.state.index]
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
                            self.next_reward(value > 0)

    def shape(self):
        """Override to fix a behavior where you need to click on the texture, which we don't want here"""

        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def validate_item_index(self):
        assert self.state.index >= 0 and self.state.index < len(
            self.config.active_inv.items
        ), f"Assert triggered on {repr(self.obj_name)}"

    def is_gomode(self):
        return self.state.is_gomode or self.state.is_gomode_light

    def next_reward(self, increase: bool):
        """Switches to the next or previous reward depending if we're incrementing or decrementing the index."""

        self.validate_item_index()
        item = self.config.active_inv.items[self.state.index]

        for i, _ in enumerate(item.positions):
            if self.obj_name.endswith(f"_pos_{i}"):
                reward = item.reward_map.get(i)

                if reward is not None and reward.item_pixmap is not None and reward.isVisible():
                    if increase:
                        self.state.infos.reward_index += 1

                        if self.state.infos.reward_index > len(self.config.active_inv.rewards.items) - 1:
                            self.state.infos.reward_index = 0
                    else:
                        self.state.infos.reward_index -= 1

                        if self.state.infos.reward_index < 0:
                            self.state.infos.reward_index = len(self.config.active_inv.rewards.items) - 1

                    item.update_reward(i, self.config.active_inv.rewards.items[self.state.infos.reward_index])

    def update_gomode(self, gomode_visibility: Optional[bool] = None):
        """Shows or hides the go-mode thing depending on the previous state."""

        assert self.effect is not None, "effect is unassigned"
        gomode_settings = self.config.gomode_settings
        cond = gomode_visibility if gomode_visibility is not None else self.effect.strength() > 0.0

        if cond:
            self.effect.setStrength(0.0)
            self.setOpacity(1.0)
            self.state.infos.gomode_visibility = True
        else:
            self.effect.setStrength(1.0)
            self.setOpacity(0.001 if gomode_settings.hide_if_disabled else GLOBAL_HALF_OPACITY)
            self.state.infos.gomode_visibility = False

        if gomode_visibility is None and self.config.label_gomode_light is not None:
            self.config.label_gomode_light.setVisible(not self.config.label_gomode_light.isVisible())
            self.state.infos.gomode_light_visibility = self.config.label_gomode_light.isVisible()

    def update_item_visibility(self):
        """Handles enabling or disabling an item, disabled means the black & white filter is enabled and the opacity lowered."""

        self.validate_item_index()
        item = self.config.active_inv.items[self.state.index]
        path_index = 0

        if self.state.infos.img_index < 0:
            if self.effect is not None:
                self.effect.setStrength(1.0)  # enable filter
            self.setOpacity(GLOBAL_HALF_OPACITY)
            path_index = 0
            item.enabled = False
        else:
            if self.effect is not None:
                self.effect.setStrength(0.0)  # disable filter
            self.setOpacity(1.0)
            path_index = self.state.infos.img_index
            item.enabled = True

        self.state.infos.enabled = item.enabled
        self.setPixmap(QPixmap(str(item.sources[path_index].path)))

    def update_flag(self, force_is_max: bool = False):
        """
        Updates the flag, flags are special text used (for OoT) to display the H/L on the hookshot or the MQ texts.
        Note: this is just an example of usage, it can be used for other purposes probably.
        """

        self.validate_item_index()
        item = self.config.active_inv.items[self.state.index]

        if self.flag is not None and item.flag_index is not None:
            flag = self.config.flags[item.flag_index]
            total = len(flag.texts) - 1

            if self.state.infos.flag_text_index > total:
                self.state.infos.flag_text_index = 0
            if self.state.infos.flag_text_index < 0:
                self.state.infos.flag_text_index = total

            self.flag.setPlainText(flag.texts[self.state.infos.flag_text_index])
            is_max = self.state.infos.flag_text_index == total if not force_is_max else False
            self.flag.set_text_style(flag.text_settings_index, is_max)

    def update_item(self, increase: bool, middle_click: bool = False):
        """
        Main item update function, Left and Right clicks are used to increment and decrement values,
        Middle clicks are used to perform other actions.
        """

        item = self.config.active_inv.items[self.state.index]
        self.validate_item_index()

        if not middle_click and len(item.sources) > 1:
            # items using multiple images, like bottles on OoT
            if increase:
                self.state.infos.img_index += 1
                self.state.infos.flag_text_index += 1
            else:
                self.state.infos.img_index -= 1
                self.state.infos.flag_text_index -= 1

            self.update_flag()

            if self.state.infos.img_index > len(item.sources) - 1:
                self.state.infos.img_index = -1
            if self.state.infos.img_index < -1:
                self.state.infos.img_index = len(item.sources) - 1

            self.update_item_visibility()
        elif self.label_counter is not None and item.counter is not None:
            # items with counters
            if increase:
                item.counter.incr(middle_click)
            else:
                item.counter.decr()

            item.counter.update(self)
            item.enabled = item.counter.show
            self.state.infos.enabled = item.enabled
            self.state.infos.counter_show = item.counter.show
            self.state.infos.counter_value = item.counter.value
        elif self.effect is not None:
            # normal items
            if self.effect.strength() > 0.0:
                self.effect.setStrength(0.0)
                self.setOpacity(1.0)
                self.state.infos.enabled = True
            else:
                self.effect.setStrength(1.0)
                self.setOpacity(GLOBAL_HALF_OPACITY)
                self.state.infos.enabled = False

    def apply_state(self):
        """Updates the item based on the `State` values. Basically combines the different update functions without the increment stuff."""

        if self.is_gomode() or self.state.index >= 0 and "extra_img" not in self.state.name:
            item = self.config.active_inv.items[self.state.index]

            if item.is_reward:
                # rewards
                for i, _ in enumerate(item.positions):
                    if self.obj_name.endswith(f"_pos_{i}"):
                        reward = item.reward_map.get(i)

                        if reward is not None and reward.item_pixmap is not None:
                            item.update_reward(i, self.config.active_inv.rewards.items[self.state.infos.reward_index])

                if self.flag is not None:
                    self.flag.setVisible(self.state.infos.show_flag)

            if self.state.is_gomode:
                # go-mode image
                gomode_settings = self.config.gomode_settings
                assert self.effect is not None, "effect is unassigned"

                if self.state.infos.gomode_visibility:
                    self.effect.setStrength(0.0)
                    self.setOpacity(1.0)
                else:
                    self.effect.setStrength(1.0)
                    self.setOpacity(0.001 if gomode_settings.hide_if_disabled else GLOBAL_HALF_OPACITY)

                # go-mode light
                if self.config.label_gomode_light is not None:
                    self.config.label_gomode_light.setVisible(self.state.infos.gomode_light_visibility)
            elif len(item.sources) > 1:
                # items using multiple images (like OoT bottles)
                self.update_flag()
                self.update_item_visibility()
            elif self.label_counter is not None and item.counter is not None:
                # items with a counter
                item.counter.show = self.state.infos.counter_show
                item.counter.value = self.state.infos.counter_value
                item.counter.update(self)
            elif self.extra is not None:
                # item extras (like the checkmark on OoT songs)
                self.extra.setVisible(self.state.infos.show_extra_img)
            elif not self.is_gomode():
                # normal items
                if self.state.infos.enabled:
                    if self.effect is not None:
                        self.effect.setStrength(0.0)
                    self.setOpacity(1.0)
                else:
                    if self.effect is not None:
                        self.effect.setStrength(1.0)
                    self.setOpacity(GLOBAL_HALF_OPACITY)

            item.enabled = self.state.infos.enabled


# from https://stackoverflow.com/a/78362730
class OutlinedGraphicsTextItem(QGraphicsTextItem):
    """Custom `QGraphicsTextItem` used to display a text with an outside outline."""

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

    def set_max_width(self, string: str):
        """Sets the max width based on the longest string possible."""

        prev = self.toPlainText()
        self.setPlainText(string)

        doc = self.document()
        self.setTextWidth(doc.size().width())
        option = doc.defaultTextOption()
        option.setAlignment(Qt.AlignmentFlag.AlignCenter)
        doc.setDefaultTextOption(option)
        self.setDocument(doc)

        self.setPlainText(prev)

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
        """See `PixmalItem.mousePressEvent`."""

        if event is not None and self.item_pixmap is not None:
            self.item_pixmap.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Completely useless for the end users currently, it prints the position of the item.
        It's useful when items are set to be moveable.
        """

        super().mouseReleaseEvent(event)
        debug_print("new pos:", self.pos())

    def wheelEvent(self, event):
        """See `PixmalItem.wheelEvent`."""

        if event is not None and self.item_pixmap is not None:
            self.item_pixmap.wheelEvent(event)

    def update_format(self, font: QFont, color: QColor):
        """Sets the font and the color of the text."""

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
        """Applies the new style on the widget based on the config settings."""

        text_settings = self.config.get_text_settings(text_settings_index)
        font = self.config.get_font(text_settings)
        color = self.config.get_color(text_settings, is_max)
        self.outline_size = text_settings.outline_thickness * 2
        self.update_format(
            QFont(font.name, int(text_settings.size), 75 if text_settings.bold else 1), Color.convert(color)
        )


class Color:
    """Simple color class used to get RGB values and convert them easily."""

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def unpack(value: int):
        """Get a new `Color` element from an hexadecimal value (0xRRGGBB)."""

        return Color((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)

    @staticmethod
    def pack(color: "Color"):
        """Get an hexadecimal value (well, actually it's an int but whatever) from the provided `Color` element."""

        return ((color.r & 0xFF) << 16) | ((color.g & 0xFF) << 8) | (color.b & 0xFF)

    @staticmethod
    def convert(color: "Color"):
        """Converts the provided color to a `QColor`."""

        return QColor(color.r, color.g, color.b)

    @staticmethod
    def to_css(color: "Color"):
        """Converts the provided color to CSS stylesheet"""

        return f"rgb({color.r}, {color.g}, {color.b})"


@dataclass
class Pos:
    """Simple class to handle a 2-axis position."""

    x: int
    y: int

    def to_str(self):
        """Format of the `Pos` attribute used by the config"""

        return f"{self.x};{self.y}"


def show_message(parent: QWidget, title: str, icon: QMessageBox.Icon, text: str):
    """Shows a message."""

    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setIcon(icon)
    message_box.setText(text)

    # correct position
    qtRectangle = message_box.frameGeometry()
    centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    message_box.move(qtRectangle.topLeft())

    message_box.show()


def show_error(parent: QWidget, text: str):
    """Shows an error message."""

    show_message(parent, "Error", QMessageBox.Icon.Critical, text)


def show_info(parent: QWidget, text: str):
    """Shows a normal message with an information."""

    show_message(parent, "Info", QMessageBox.Icon.Information, text)


def move_file_to_config(config: "Config", path: Path):
    config_folder = config.config_path.parent

    if not path.is_relative_to(config_folder):
        dest = config_folder / "auto_copied" / f"{path.stem}{path.suffix}"
        copyfile(path, dest)
        assert dest.exists(), "unknown file copy failure"
        path = dest

    return path


def debug_print(msg: str):
    if DEBUG_PRINTS:
        print(msg)
