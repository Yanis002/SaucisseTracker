import os

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QPushButton,
    QFontComboBox,
    QFileDialog,
)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontDatabase

from config import Config, Font, FlagItem, ExtraItem, RewardItem
from common import Pos, move_file_to_config

if TYPE_CHECKING:
    from editor import TrackerEditorMenu


class TextSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.config = config

        self.label_item_index = QLabel("Item Index", self)
        self.label_item_index.setGeometry(9, 10, 71, 18)

        self.item_index = QSpinBox(self)
        self.item_index.setGeometry(10, 30, 61, 32)
        self.item_index.setMinimum(1)
        self.item_index.setMaximum(len(self.config.text_settings))
        self.item_index.valueChanged.connect(self.item_value_changed)

        self.btn_item_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self)
        self.btn_item_add.setGeometry(80, 30, 41, 33)
        self.btn_item_add.pressed.connect(self.item_add)

        self.btn_item_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self)
        self.btn_item_del.setGeometry(130, 30, 41, 33)
        self.btn_item_del.pressed.connect(self.item_del)

        self.group_item_settings = QGroupBox(
            f"Item Settings ({self.item_index.value()} / {len(self.config.text_settings)})", self
        )
        self.group_item_settings.setGeometry(10, 70, 241, 321)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 400, 241, 32)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.btn_ok_cancel.accepted.connect(self.accept)

    def item_value_changed(self, value: int):
        index = self.item_index.value()

        self.group_item_settings.setTitle(f"Item Settings ({index} / {len(self.config.fonts)})")

    def item_add(self):
        pass

    def item_del(self):
        pass

    def accept(self):
        super().accept()


class GoModeSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: "TrackerEditorMenu"):
        super().__init__(parent)

        self.config = config
        self.editor = parent
        self.pause_update = True

        self.group_text = QGroupBox("Text", self)
        self.group_text.setGeometry(10, 10, 315, 108)

        self.label_pos_x = QLabel("X", self.group_text)
        self.label_pos_x.setGeometry(33, 26, 21, 18)
        self.icon_pos_x = QSpinBox(self.group_text)
        self.icon_pos_x.setGeometry(8, 46, 55, 32)
        self.icon_pos_x.setMinimum(-999)
        self.icon_pos_x.setMaximum(999)
        self.icon_pos_x.valueChanged.connect(self.update_icon_pos)

        self.label_pos_y = QLabel("Y", self.group_text)
        self.label_pos_y.setGeometry(92, 26, 21, 18)
        self.icon_pos_y = QSpinBox(self.group_text)
        self.icon_pos_y.setGeometry(68, 46, 55, 32)
        self.icon_pos_y.setMinimum(-999)
        self.icon_pos_y.setMaximum(999)
        self.icon_pos_y.valueChanged.connect(self.update_icon_pos)

        self.label_path = QLabel("Icon Path", self.group_text)
        self.label_path.setGeometry(160, 26, 81, 18)
        self.icon_path = QLineEdit(self.group_text)
        self.icon_path.setGeometry(128, 46, 115, 32)
        self.icon_path.setReadOnly(True)
        self.btn_set_path = QPushButton("Set Path", self.group_text)
        self.btn_set_path.setGeometry(247, 45, 61, 34)
        self.btn_set_path.pressed.connect(self.open_icon_path)

        self.hide_if_disabled = QCheckBox("Hide if disabled", self.group_text)
        self.hide_if_disabled.setGeometry(6, 80, 121, 22)

        self.group_light = QGroupBox("Use Light", self)
        self.group_light.setGeometry(10, 130, 315, 173)
        self.group_light.setCheckable(True)

        self.label_light_pos_x = QLabel("X", self.group_light)
        self.label_light_pos_x.setGeometry(33, 30, 21, 18)
        self.light_pos_x = QSpinBox(self.group_light)
        self.light_pos_x.setGeometry(8, 50, 55, 32)
        self.light_pos_x.setMinimum(-999)
        self.light_pos_x.setMaximum(999)
        self.light_pos_x.valueChanged.connect(self.update_light_pos)

        self.label_light_pos_y = QLabel("Y", self.group_light)
        self.label_light_pos_y.setGeometry(92, 30, 21, 18)
        self.light_pos_y = QSpinBox(self.group_light)
        self.light_pos_y.setGeometry(68, 50, 55, 32)
        self.light_pos_y.setMinimum(-999)
        self.light_pos_y.setMaximum(999)
        self.light_pos_y.valueChanged.connect(self.update_light_pos)

        self.label_light_path = QLabel("Image Path", self.group_light)
        self.label_light_path.setGeometry(150, 30, 81, 18)
        self.light_path = QLineEdit(self.group_light)
        self.light_path.setGeometry(128, 50, 115, 32)
        self.light_path.setReadOnly(True)
        self.btn_set_light_path = QPushButton("Set Path", self.group_light)
        self.btn_set_light_path.setGeometry(247, 49, 61, 34)
        self.btn_set_light_path.pressed.connect(self.open_light_img_path)

        self.label_rot_speed = QLabel("Rotation Speed", self.group_light)
        self.label_rot_speed.setGeometry(10, 97, 101, 18)
        self.rot_speed = QSpinBox(self.group_light)
        self.rot_speed.setGeometry(154, 90, 55, 32)
        self.rot_speed.setMinimum(-999)
        self.rot_speed.setMaximum(999)
        self.rot_speed.valueChanged.connect(self.update_rotation)

        self.label_rot_refresh = QLabel("Rotation Refresh Value", self.group_light)
        self.label_rot_refresh.setGeometry(10, 136, 141, 18)
        self.rot_refresh = QDoubleSpinBox(self.group_light)
        self.rot_refresh.setGeometry(154, 130, 71, 32)
        self.rot_refresh.setDecimals(3)
        self.rot_refresh.setSingleStep(0.001)
        self.rot_refresh.setMaximum(1.0)
        self.rot_refresh.valueChanged.connect(self.update_rotation)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 310, 315, 31)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.btn_ok_cancel.accepted.connect(self.accept)

        self.icon_pos_x.setValue(self.config.gomode_settings.pos.x)
        self.icon_pos_y.setValue(self.config.gomode_settings.pos.y)
        self.icon_path.setText(str(self.config.gomode_settings.path))

        self.light_pos_x.setValue(self.config.gomode_settings.light_pos.x)
        self.light_pos_y.setValue(self.config.gomode_settings.light_pos.y)
        self.light_path.setText(str(self.config.gomode_settings.light_path))

        self.rot_speed.setValue(self.config.gomode_settings.rotation_speed)
        self.rot_refresh.setValue(self.config.gomode_settings.thread_refresh_rate)

        self.pause_update = False
        self.setFixedSize(334, 347)
        self.setWindowTitle("Go Mode Settings")

    def update_scene(self):
        self.editor.tracker.task_rotation.position = 0
        self.editor.tracker.task_rotation.speed = self.config.gomode_settings.rotation_speed
        self.editor.tracker.task_rotation.thread_refresh = self.config.gomode_settings.thread_refresh_rate

        if self.config.label_gomode is not None:
            self.editor.tracker.scene.removeItem(self.config.label_gomode)
            self.config.label_gomode = None

        if self.config.label_gomode_light is not None:
            self.editor.tracker.scene.removeItem(self.config.label_gomode_light)
            self.config.label_gomode_light = None

        self.editor.tracker.create_gomode(self.hide_if_disabled.isChecked())

    def update_icon_pos(self, value: int):
        if self.pause_update:
            return

        self.config.gomode_settings.pos.x = self.icon_pos_x.value()
        self.config.gomode_settings.pos.y = self.icon_pos_y.value()
        self.update_scene()

    def open_icon_path(self):
        path_str = QFileDialog.getOpenFileName(
            self, "Open Go Mode Icon", str(self.config.gomode_settings.path.parent), "*.png"
        )[0]

        if len(path_str) == 0:
            return

        path = Path(path_str).resolve()
        assert path.exists(), "path doesn't exist!"
        path = move_file_to_config(self.config, path)

        self.config.gomode_settings.path = path
        self.update_scene()

    def update_light_pos(self, value: int):
        if self.pause_update:
            return

        self.config.gomode_settings.light_pos.x = self.light_pos_x.value()
        self.config.gomode_settings.light_pos.y = self.light_pos_y.value()
        self.update_scene()

    def open_light_img_path(self):
        path_str = QFileDialog.getOpenFileName(
            self, "Open Go Mode Light Image", str(self.config.gomode_settings.light_path.parent), "*.png"
        )[0]

        if len(path_str) == 0:
            return

        path = Path(path_str).resolve()
        assert path.exists(), "path doesn't exist!"
        path = move_file_to_config(self.config, path)

        self.config.gomode_settings.light_path = path
        self.update_scene()

    def update_rotation(self, value: int):
        if self.pause_update:
            return

        self.config.gomode_settings.rotation_speed = self.rot_speed.value()
        self.config.gomode_settings.thread_refresh_rate = self.rot_refresh.value()
        self.update_scene()


class RewardSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.config = config
        self.pause_update = False

        self.label_item_index = QLabel("Item Index", self)
        self.label_item_index.setGeometry(9, 10, 71, 18)

        self.item_index = QSpinBox(self)
        self.item_index.setGeometry(10, 30, 61, 32)
        self.item_index.setMinimum(1)
        self.item_index.setMaximum(len(self.config.active_inv.rewards.items))
        self.item_index.valueChanged.connect(self.item_value_changed)

        self.btn_item_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self)
        self.btn_item_add.setGeometry(80, 30, 41, 33)
        self.btn_item_add.pressed.connect(self.item_add)

        self.btn_item_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self)
        self.btn_item_del.setGeometry(130, 30, 41, 33)
        self.btn_item_del.pressed.connect(self.item_del)

        self.group_item_settings = QGroupBox(
            f"Item Settings ({self.item_index.value()} / {len(self.config.active_inv.rewards.items)})", self
        )
        self.group_item_settings.setGeometry(10, 70, 261, 145)

        self.label_name = QLabel("Name", self.group_item_settings)
        self.label_name.setGeometry(50, 30, 51, 18)
        self.name = QLineEdit(self.group_item_settings)
        self.name.setGeometry(10, 50, 115, 32)
        self.name.textChanged.connect(self.name_update)

        self.label_text_settings_index = QLabel("Text Settings Index", self.group_item_settings)
        self.label_text_settings_index.setGeometry(133, 30, 121, 18)
        self.text_settings_index = QSpinBox(self.group_item_settings)
        self.text_settings_index.setGeometry(130, 50, 115, 32)
        self.text_settings_index.valueChanged.connect(self.text_index_update)

        self.label_pos_x = QLabel("X", self.group_item_settings)
        self.label_pos_x.setGeometry(95, 83, 21, 18)
        self.item_pos_x = QSpinBox(self.group_item_settings)
        self.item_pos_x.setGeometry(70, 103, 55, 32)
        self.item_pos_x.setMinimum(-999)
        self.item_pos_x.setMaximum(999)
        self.item_pos_x.valueChanged.connect(self.update_reward)

        self.label_pos_y = QLabel("Y", self.group_item_settings)
        self.label_pos_y.setGeometry(154, 83, 21, 18)
        self.item_pos_y = QSpinBox(self.group_item_settings)
        self.item_pos_y.setGeometry(130, 103, 55, 32)
        self.item_pos_y.setMinimum(-999)
        self.item_pos_y.setMaximum(999)
        self.item_pos_y.valueChanged.connect(self.update_reward)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 220, 261, 32)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.btn_ok_cancel.accepted.connect(self.accept)

        self.item_value_changed(1)
        self.setFixedSize(282, 260)
        self.setWindowTitle("Reward Settings")

    def update_scene(self):
        offset = -1 if os.name == "nt" else 0
        active_inv = self.config.active_inv

        for item in active_inv.items:
            for i, pixmap_item in enumerate(item.pixmap_items):
                if i in item.reward_map:
                    reward_info = active_inv.rewards.items[item.pixmap_items[i].state.infos.reward_index]

                    pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)
                    pos.x += reward_info.pos.x
                    pos.y += reward_info.pos.y

                    item.reward_map[i].setPlainText(reward_info.name)
                    item.reward_map[i].set_text_style(reward_info.text_settings_index, False)
                    item.reward_map[i].setPos(float(pos.x), float(pos.y))
                    item.reward_map[i].set_max_width(active_inv.rewards.get_longest_reward())

    def item_value_changed(self, value: int):
        index = self.item_index.value()

        self.group_item_settings.setTitle(f"Item Settings ({index} / {len(self.config.active_inv.rewards.items)})")

        self.pause_update = True
        reward_info = self.config.active_inv.rewards.items[index - 1]
        self.name.setText(reward_info.name)
        self.text_settings_index.setValue(reward_info.text_settings_index)
        self.item_pos_x.setValue(reward_info.pos.x)
        self.item_pos_y.setValue(reward_info.pos.y)
        self.pause_update = False

    def item_add(self):
        index = len(self.config.active_inv.rewards.items)
        self.config.active_inv.rewards.items.append(RewardItem(index - 1, Pos(0, 0), Path()))
        self.item_index.setMaximum(len(self.config.active_inv.rewards.items))
        self.item_index.setValue(index + 1)

    def item_del(self):
        index = self.item_index.value()
        self.config.active_inv.rewards.items.pop(index - 1)
        self.item_index.setMaximum(len(self.config.active_inv.rewards.items))
        self.item_index.setValue(index - 1)

    def name_update(self, text):
        index = self.item_index.value()

        if self.pause_update:
            return

        self.config.active_inv.rewards.items[index - 1].name = self.name.text()
        self.update_scene()

    def text_index_update(self, value: int):
        index = self.item_index.value()

        if self.pause_update:
            return

        self.config.active_inv.rewards.items[index - 1].text_settings_index = self.text_settings_index.value()
        self.update_scene()

    def update_reward(self):
        index = self.item_index.value()

        if self.pause_update:
            return

        self.config.active_inv.rewards.items[index - 1].pos.x = self.item_pos_x.value()
        self.config.active_inv.rewards.items[index - 1].pos.y = self.item_pos_y.value()
        self.update_scene()


class ExtraSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: "TrackerEditorMenu"):
        super().__init__(parent)

        self.config = config
        self.editor = parent
        self.pause_update = False

        self.label_item_index = QLabel("Item Index", self)
        self.label_item_index.setGeometry(9, 10, 71, 18)

        self.item_index = QSpinBox(self)
        self.item_index.setGeometry(10, 30, 61, 32)
        self.item_index.setMinimum(1)
        self.item_index.setMaximum(len(self.config.extras.items))
        self.item_index.valueChanged.connect(self.item_value_changed)

        self.btn_item_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self)
        self.btn_item_add.setGeometry(80, 30, 41, 33)
        self.btn_item_add.pressed.connect(self.item_add)

        self.btn_item_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self)
        self.btn_item_del.setGeometry(130, 30, 41, 33)
        self.btn_item_del.pressed.connect(self.item_del)

        self.group_item_settings = QGroupBox(
            f"Item Settings ({self.item_index.value()} / {len(self.config.extras.items)})", self
        )
        self.group_item_settings.setGeometry(10, 70, 181, 145)

        self.label_icon_path = QLabel("Icon Path", self.group_item_settings)
        self.label_icon_path.setGeometry(12, 30, 61, 18)
        self.icon_path = QLineEdit(self.group_item_settings)
        self.icon_path.setGeometry(10, 50, 115, 32)
        self.icon_path.setReadOnly(True)

        self.btn_set_path = QPushButton("Set", self.group_item_settings)
        self.btn_set_path.setGeometry(130, 49, 41, 34)
        self.btn_set_path.pressed.connect(self.set_icon_path)

        self.label_pos_x = QLabel("X", self.group_item_settings)
        self.label_pos_x.setGeometry(53, 83, 21, 18)
        self.item_pos_x = QSpinBox(self.group_item_settings)
        self.item_pos_x.setGeometry(28, 103, 55, 32)
        self.item_pos_x.setMinimum(-999)
        self.item_pos_x.setMaximum(999)
        self.item_pos_x.valueChanged.connect(self.update_extra)

        self.label_pos_y = QLabel("Y", self.group_item_settings)
        self.label_pos_y.setGeometry(120, 83, 21, 18)
        self.item_pos_y = QSpinBox(self.group_item_settings)
        self.item_pos_y.setGeometry(96, 103, 55, 32)
        self.item_pos_y.setMinimum(-999)
        self.item_pos_y.setMaximum(999)
        self.item_pos_y.valueChanged.connect(self.update_extra)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 220, 181, 32)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.btn_ok_cancel.accepted.connect(self.accept)

        self.item_value_changed(1)
        self.setFixedSize(201, 260)
        self.setWindowTitle("Extra Settings")

    def accept(self):
        self.editor.extra_index.setMaximum(len(self.config.extras.items) - 1)
        super().accept()

    def update_scene(self):
        offset = -1 if os.name == "nt" else 0

        for item in self.config.active_inv.items:
            if item.extra_index is not None:
                for i, pixmap_item in enumerate(item.pixmap_items):
                    if pixmap_item.extra is not None:
                        self.editor.tracker.scene.removeItem(pixmap_item.extra)
                        pixmap_item.extra = None
                        pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)
                        self.editor.tracker.create_extra(item, i, pixmap_item.obj_name, pos)
                        self.editor.update_extras_enabled(self.editor.group_extras.isChecked())

    def item_value_changed(self, value: int):
        index = self.item_index.value()

        self.group_item_settings.setTitle(f"Item Settings ({index} / {len(self.config.extras.items)})")
        self.pause_update = True
        extra = self.config.extras.items[index - 1]
        self.icon_path.setText(str(extra.path))
        self.item_pos_x.setValue(extra.pos.x)
        self.item_pos_y.setValue(extra.pos.y)
        self.pause_update = False

    def item_add(self):
        index = len(self.config.extras.items)
        self.config.extras.items.append(ExtraItem(index - 1, Pos(0, 0), Path()))
        self.item_index.setMaximum(len(self.config.extras.items))
        self.item_index.setValue(index + 1)

    def item_del(self):
        index = self.item_index.value()
        self.config.extras.items.pop(index - 1)
        self.item_index.setMaximum(len(self.config.extras.items))
        self.item_index.setValue(index - 1)

    def update_extra(self):
        index = self.item_index.value()

        if self.pause_update:
            return

        self.config.extras.items[index - 1].pos.x = self.item_pos_x.value()
        self.config.extras.items[index - 1].pos.y = self.item_pos_y.value()
        self.update_scene()

    def set_icon_path(self):
        index = self.item_index.value() - 1
        path_str = QFileDialog.getOpenFileName(
            self, "Select Image File", str(self.config.extras.items[index].path.parent), "Images (*.png)"
        )[0]

        if len(path_str) == 0:
            return

        path = Path(path_str).resolve()
        assert path.exists(), "path doesn't exist!"
        path = move_file_to_config(self.config, path)

        self.config.extras.items[index].path = path
        self.icon_path.setText(str(path))
        self.update_scene()


class FlagSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: "TrackerEditorMenu"):
        super().__init__(parent)

        self.config = config
        self.editor = parent
        self.pause_update = False

        self.label_item_index = QLabel("Item Index", self)
        self.label_item_index.setGeometry(9, 10, 71, 18)

        self.item_index = QSpinBox(self)
        self.item_index.setGeometry(10, 30, 61, 32)
        self.item_index.setMinimum(1)
        self.item_index.setMaximum(len(self.config.flags))
        self.item_index.valueChanged.connect(self.item_value_changed)

        self.btn_item_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self)
        self.btn_item_add.setGeometry(80, 30, 41, 33)
        self.btn_item_add.pressed.connect(self.item_add)

        self.btn_item_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self)
        self.btn_item_del.setGeometry(130, 30, 41, 33)
        self.btn_item_del.pressed.connect(self.item_del)

        self.group_item_settings = QGroupBox(
            f"Item Settings ({self.item_index.value()} / {self.item_index.maximum()})", self
        )
        self.group_item_settings.setGeometry(10, 70, 191, 311)

        self.label_pos_x = QLabel("X", self.group_item_settings)
        self.label_pos_x.setGeometry(37, 30, 21, 18)
        self.item_pos_x = QSpinBox(self.group_item_settings)
        self.item_pos_x.setGeometry(12, 50, 55, 32)
        self.item_pos_x.setMinimum(-999)
        self.item_pos_x.setMaximum(999)
        self.item_pos_x.valueChanged.connect(self.update_flag)

        self.label_pos_y = QLabel("Y", self.group_item_settings)
        self.label_pos_y.setGeometry(96, 30, 21, 18)
        self.item_pos_y = QSpinBox(self.group_item_settings)
        self.item_pos_y.setGeometry(72, 50, 55, 32)
        self.item_pos_y.setMinimum(-999)
        self.item_pos_y.setMaximum(999)
        self.item_pos_y.valueChanged.connect(self.update_flag)

        self.label_text_settings_index = QLabel("Text Settings Index", self.group_item_settings)
        self.label_text_settings_index.setGeometry(13, 87, 121, 18)
        self.text_settings_index = QSpinBox(self.group_item_settings)
        self.text_settings_index.setGeometry(10, 107, 115, 32)
        self.text_settings_index.valueChanged.connect(self.update_flag)

        self.is_hidden = QCheckBox("Is Hidden", self.group_item_settings)
        self.is_hidden.setGeometry(10, 280, 100, 22)
        self.is_hidden.checkStateChanged.connect(self.hidden_update)

        self.group_text_list = QGroupBox("Text List", self.group_item_settings)
        self.group_text_list.setGeometry(10, 147, 171, 128)

        self.btn_text_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self.group_text_list)
        self.btn_text_add.setGeometry(72, 50, 41, 33)
        self.btn_text_add.pressed.connect(self.text_add)

        self.btn_text_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self.group_text_list)
        self.btn_text_del.setGeometry(118, 50, 41, 33)
        self.btn_text_del.pressed.connect(self.text_del)

        self.label_text_index = QLabel("Text Index", self.group_text_list)
        self.label_text_index.setGeometry(4, 30, 71, 18)
        self.text_index = QSpinBox(self.group_text_list)
        self.text_index.setGeometry(5, 50, 61, 32)
        self.text_index.setMinimum(1)
        self.text_index.setMaximum(len(self.config.flags[self.item_index.value()].texts))
        self.text_index.valueChanged.connect(self.text_value_changed)

        self.label_text_total = QLabel(f"Total: {self.text_index.maximum()}", self.group_text_list)
        self.label_text_total.setGeometry(99, 30, 58, 18)
        self.label_text_total.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )

        self.text = QLineEdit(self.group_text_list)
        self.text.setGeometry(5, 90, 161, 32)
        self.text.textChanged.connect(self.text_update)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 390, 191, 31)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.btn_ok_cancel.accepted.connect(self.accept)

        self.item_value_changed(1)
        self.setFixedSize(212, 430)
        self.setWindowTitle("Flag Settings")

    def accept(self):
        self.editor.flag_index.setMaximum(len(self.config.flags) - 1)
        super().accept()

    def update_scene(self):
        offset = -1 if os.name == "nt" else 0

        for item in self.config.active_inv.items:
            if item.flag_index is not None:
                flag = self.config.flags[item.flag_index]

                for i, pixmap_item in enumerate(item.pixmap_items):
                    pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)
                    pos.x += flag.pos.x
                    pos.y += flag.pos.y

                    if pixmap_item.flag is not None:
                        is_visible = pixmap_item.flag.isVisible()
                        pixmap_item.flag.setPos(float(pos.x), float(pos.y))
                        pixmap_item.flag.set_text_style(flag.text_settings_index, False)
                        pixmap_item.flag.setPlainText(flag.texts[pixmap_item.state.infos.flag_text_index])
                        pixmap_item.flag.set_max_width(flag.get_longest_flag())
                        pixmap_item.flag.setVisible(is_visible)

    def item_value_changed(self, value: int):
        index = self.item_index.value()

        self.group_item_settings.setTitle(f"Item Settings ({index} / {self.item_index.maximum()})")

        flag = self.config.flags[index - 1]
        self.pause_update = True
        self.item_pos_x.setValue(flag.pos.x)
        self.item_pos_y.setValue(flag.pos.y)
        self.label_text_total.setText(f"Total: {len(flag.texts)}")
        self.text_index.setMaximum(len(flag.texts))
        self.text_settings_index.setValue(flag.text_settings_index)
        self.text.setText(flag.texts[self.text_index.value() - 1])
        self.is_hidden.setChecked(flag.hidden)
        self.pause_update = False

    def item_add(self):
        index = len(self.config.flags)
        self.config.flags.append(FlagItem(index - 1, [""], Pos(0, 0), 0, False, 0, 0))
        self.item_index.setMaximum(len(self.config.flags))
        self.item_index.setValue(index + 1)

        self.text_index.setMaximum(1)
        self.text_index.setValue(1)

    def item_del(self):
        index = self.item_index.value()
        self.config.flags.pop(index - 1)
        self.item_index.setMaximum(len(self.config.flags))
        self.item_index.setValue(index - 1)

        flag = self.config.flags[index - 1 - 1]
        self.text_index.setMaximum(len(flag.texts))
        self.text_index.setValue(1)

    def text_value_changed(self, value: int):
        index = self.text_index.value() - 1
        self.text.setText(self.config.flags[self.item_index.value() - 1].texts[index])

    def text_update(self, text: str):
        index = self.text_index.value() - 1
        self.config.flags[self.item_index.value() - 1].texts[index] = self.text.text()
        self.update_scene()

    def text_add(self):
        item_index = self.item_index.value() - 1
        self.config.flags[item_index].texts.append(str())
        self.text_index.setMaximum(len(self.config.flags[item_index].texts))
        self.text_index.setValue(1)

    def text_del(self):
        item_index = self.item_index.value() - 1
        index = self.text_index.value() - 1
        self.config.flags[item_index].texts.pop(index)
        self.text_index.setMaximum(len(self.config.flags[item_index].texts))
        self.text_index.setValue(1)

    def hidden_update(self):
        item_index = self.item_index.value() - 1

        if self.pause_update:
            return

        self.config.flags[item_index].hidden = self.is_hidden.isChecked()

    def update_flag(self):
        item_index = self.item_index.value() - 1

        if self.pause_update:
            return

        self.config.flags[item_index].pos.x = self.item_pos_x.value()
        self.config.flags[item_index].pos.y = self.item_pos_y.value()
        self.config.flags[item_index].text_settings_index = self.text_settings_index.value()
        self.update_scene()


class FontSettingsDialog(QDialog):
    def __init__(self, config: Config, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.config = config

        self.label_item_index = QLabel("Item Index", self)
        self.label_item_index.setGeometry(9, 10, 71, 18)

        self.item_index = QSpinBox(self)
        self.item_index.setGeometry(10, 30, 61, 32)
        self.item_index.setMinimum(1)
        self.item_index.setMaximum(len(self.config.fonts))
        self.item_index.valueChanged.connect(self.item_value_changed)

        self.btn_item_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self)
        self.btn_item_add.setGeometry(80, 30, 41, 33)
        self.btn_item_add.pressed.connect(self.item_add)

        self.btn_item_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self)
        self.btn_item_del.setGeometry(130, 30, 41, 33)
        self.btn_item_del.pressed.connect(self.item_del)

        self.group_item_settings = QGroupBox(
            f"Item Settings ({self.item_index.value()} / {len(self.config.fonts)})", self
        )
        self.group_item_settings.setGeometry(10, 70, 251, 141)

        self.is_custom = QCheckBox("Use Custom Font File", self.group_item_settings)
        self.is_custom.setGeometry(10, 30, 171, 22)
        self.is_custom.checkStateChanged.connect(self.toggle_custom)

        self.custom_font_path = QLineEdit(self.group_item_settings)
        self.custom_font_path.setGeometry(10, 60, 171, 32)
        self.custom_font_path.setReadOnly(True)

        self.btn_set_path = QPushButton("Set Path", self.group_item_settings)
        self.btn_set_path.setGeometry(181, 59, 61, 34)
        self.btn_set_path.pressed.connect(self.set_font_path)

        self.combo_font = QFontComboBox(self.group_item_settings)
        self.combo_font.setGeometry(10, 100, 231, 32)

        self.btn_ok_cancel = QDialogButtonBox(self)
        self.btn_ok_cancel.setGeometry(10, 220, 251, 32)
        self.btn_ok_cancel.setOrientation(Qt.Orientation.Horizontal)
        self.btn_ok_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.btn_ok_cancel.accepted.connect(self.accept)

        self.is_custom.setChecked(True)
        self.setFixedSize(270, 260)
        self.setWindowTitle("Font Settings")

    def set_font_path(self):
        index = self.item_index.value() - 1
        path_str = QFileDialog.getOpenFileName(
            self, "Select Font File", str(self.config.fonts[index].path.parent), "Font files (*.otf *.ttf)"
        )[0]

        if len(path_str) == 0:
            return

        path = Path(path_str).resolve()
        assert path.exists(), "path doesn't exist!"
        path = move_file_to_config(self.config, path)

        if self.config.fonts[index].font_id != -1:
            QFontDatabase.removeApplicationFont(self.config.fonts[index].font_id)

        font_id = QFontDatabase.addApplicationFont(str(path))
        assert font_id != -1, "font cannot be loaded"
        self.config.fonts[index].path = path
        self.config.fonts[index].name = QFontDatabase.applicationFontFamilies(font_id)[0]

    def toggle_custom(self, state):
        self.custom_font_path.setEnabled(self.is_custom.isChecked())
        self.btn_set_path.setEnabled(self.is_custom.isChecked())
        self.combo_font.setEnabled(not self.is_custom.isChecked())

    def item_value_changed(self, value: int):
        index = self.item_index.value()

        self.group_item_settings.setTitle(f"Item Settings ({index} / {len(self.config.fonts)})")
        self.is_custom.setChecked(not self.config.fonts[index - 1].is_system)
        if self.is_custom.isChecked():
            self.custom_font_path.setText(str(self.config.fonts[index - 1].path))
        else:
            pass

    def item_add(self):
        index = len(self.config.fonts)
        self.config.fonts.append(Font(self.config.widget, index, str(), Path()))
        self.item_index.setMaximum(len(self.config.fonts))
        self.item_index.setValue(index + 1)

    def item_del(self):
        index = self.item_index.value()
        self.config.fonts.pop(index - 1)
        self.item_index.setMaximum(len(self.config.fonts))
        self.item_index.setValue(index - 1)
