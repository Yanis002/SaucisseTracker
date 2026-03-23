from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QGuiApplication, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QListView,
    QPushButton,
    QSpinBox,
    QGraphicsItem,
    QFrame,
    QLineEdit,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QColorDialog,
    QFileDialog,
    QCheckBox,
)

from common import ListViewModel, Color, Pos, move_file_to_config
from config import Config, InventoryItem, Counter, SourceItem
from tracker import TrackerWindow

from editor_dialogs import (
    TextSettingsDialog,
    GoModeSettingsDialog,
    RewardSettingsDialog,
    ExtraSettingsDialog,
    FlagSettingsDialog,
    FontSettingsDialog,
)


class TrackerEditorMenu(QWidget):
    def __init__(self, config: Config, tracker: "TrackerEditor"):
        super().__init__()
        self.config = config
        self.tracker = tracker
        self.prev_item: Optional[InventoryItem] = None
        self.pause_update = False  # TODO: find something better

        first_item = self.config.active_inv.items[0]

        # items section
        self.group_items = QGroupBox("Items", self)
        self.group_items.setGeometry(10, 10, 261, 591)
        self.list_selected = QListView(self.group_items)
        self.list_selected.setGeometry(10, 32, 240, 461)

        self.model_cache: list[tuple[bool, str, QPixmap]] = []
        for item in self.config.active_inv.items:
            self.model_cache.append((True, item.name, item.pixmap_items[0].pixmap().scaled(32, 32)))
        self.list_selected.setModel(ListViewModel(self.model_cache))
        self.list_selected.setCurrentIndex(self.list_selected.model().index(0, 0))
        self.model = self.list_selected.selectionModel()
        self.model.currentChanged.connect(self.selection_changed)

        # item name, paths and sources section
        self.label_item_name = QLabel("Item Name", self.group_items)
        self.label_item_name.setGeometry(10, 531, 70, 20)
        self.item_name = QLineEdit(self.group_items)
        self.item_name.setGeometry(9, 551, 241, 32)
        self.item_name.textChanged.connect(self.update_item_name)

        self.btn_add_item = QPushButton("Add Item", self.group_items)
        self.btn_add_item.setGeometry(10, 500, 111, 34)
        self.btn_add_item.pressed.connect(self.add_item)

        self.btn_delete_item = QPushButton("Delete Item", self.group_items)
        self.btn_delete_item.setGeometry(140, 500, 111, 34)
        self.btn_delete_item.pressed.connect(self.remove_item)

        self.group_pos = QGroupBox("Positions", self)
        self.group_pos.setGeometry(410, 170, 251, 181)

        self.label_item_pos = QLabel("Pos. Index", self.group_pos)
        self.label_item_pos.setGeometry(9, 20, 71, 18)
        self.item_pos_index = QSpinBox(self.group_pos)
        self.item_pos_index.setGeometry(10, 40, 61, 32)
        self.item_pos_index.setMinimum(1)
        self.item_pos_index.setMaximum(len(first_item.positions))
        self.item_pos_index.valueChanged.connect(self.item_pos_value_changed)

        self.btn_pos_add = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd), "", self.group_pos)
        self.btn_pos_add.setGeometry(80, 40, 41, 33)
        self.btn_pos_add.pressed.connect(self.item_pos_add)
        self.btn_pos_del = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove), "", self.group_pos)
        self.btn_pos_del.setGeometry(130, 40, 41, 33)
        self.btn_pos_del.pressed.connect(self.item_pos_del)

        self.group_pos_settings = QGroupBox(
            f"Position Settings ({self.item_pos_index.value()} / {len(first_item.positions)})", self.group_pos
        )
        self.group_pos_settings.setGeometry(10, 80, 231, 91)

        self.label_pos_x = QLabel("X", self.group_pos_settings)
        self.label_pos_x.setGeometry(31, 30, 21, 18)
        self.pos_x = QSpinBox(self.group_pos_settings)
        self.pos_x.setGeometry(8, 50, 55, 32)
        self.pos_x.setMinimum(-999)
        self.pos_x.setMaximum(999)
        self.pos_x.valueChanged.connect(self.update_pos_x)

        self.label_pos_y = QLabel("Y", self.group_pos_settings)
        self.label_pos_y.setGeometry(110, 30, 21, 18)
        self.pos_y = QSpinBox(self.group_pos_settings)
        self.pos_y.setGeometry(88, 50, 55, 32)
        self.pos_y.setMinimum(-999)
        self.pos_y.setMaximum(999)
        self.pos_y.valueChanged.connect(self.update_pos_y)

        self.label_pos_y = QLabel("Angle", self.group_pos_settings)
        self.label_pos_y.setGeometry(178, 30, 41, 20)
        self.angle = QSpinBox(self.group_pos_settings)
        self.angle.setGeometry(168, 50, 55, 32)
        self.angle.setMinimum(-999)
        self.angle.setMaximum(999)
        self.angle.valueChanged.connect(self.update_angle)

        self.group_sources = QGroupBox("Icon Paths", self)
        self.group_sources.setGeometry(670, 10, 331, 511)

        self.list_sources = QListView(self.group_sources)
        self.list_sources.setGeometry(10, 30, 311, 441)

        self.model_cache_sources: list[tuple[bool, str, QPixmap]] = []
        for src_item in first_item.sources:
            self.model_cache_sources.append((True, str(src_item.path), QPixmap(str(src_item.path))))
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()
        self.model_sources.currentChanged.connect(self.sources_selection_update)

        self.btn_sources_add = QPushButton("Add", self.group_sources)
        self.btn_sources_add.setGeometry(9, 480, 71, 21)
        self.btn_sources_add.pressed.connect(self.sources_add)

        self.btn_sources_del = QPushButton("Remove", self.group_sources)
        self.btn_sources_del.setGeometry(82, 480, 71, 21)
        self.btn_sources_del.pressed.connect(self.sources_del)

        self.btn_sources_open = QPushButton("Open File", self.group_sources)
        self.btn_sources_open.setGeometry(155, 480, 71, 21)
        self.btn_sources_open.pressed.connect(self.sources_open)

        self.btn_sources_up = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.GoUp), "", self.group_sources)
        self.btn_sources_up.setGeometry(258, 480, 31, 21)
        self.btn_sources_up.pressed.connect(self.sources_move_up)

        self.btn_sources_down = QPushButton(QIcon.fromTheme(QIcon.ThemeIcon.GoDown), "", self.group_sources)
        self.btn_sources_down.setGeometry(290, 480, 31, 21)
        self.btn_sources_down.pressed.connect(self.sources_move_down)

        self.group_counters = QGroupBox("Use Counters", self)
        self.group_counters.setGeometry(410, 10, 251, 151)
        self.group_counters.setCheckable(True)
        self.group_counters.setChecked(False)
        self.group_counters.toggled.connect(self.update_counter_enabled)

        self.label_text_index = QLabel("Text Settings Index", self.group_counters)
        self.label_text_index.setGeometry(8, 30, 121, 18)
        self.counter_text_index = QSpinBox(self.group_counters)
        self.counter_text_index.setGeometry(8, 50, 115, 32)
        self.counter_text_index.setMinimum(0)
        self.counter_text_index.setMaximum(len(self.config.text_settings) - 1)
        self.counter_text_index.valueChanged.connect(self.update_counter_info)

        self.label_min = QLabel("Min.", self.group_counters)
        self.label_min.setGeometry(22, 90, 31, 18)
        self.counter_min = QSpinBox(self.group_counters)
        self.counter_min.setGeometry(8, 110, 55, 32)
        self.counter_min.setMinimum(0)
        self.counter_min.valueChanged.connect(self.update_counter_info)

        self.label_max = QLabel("Max.", self.group_counters)
        self.label_max.setGeometry(79, 90, 41, 18)
        self.counter_max = QSpinBox(self.group_counters)
        self.counter_max.setGeometry(68, 110, 55, 32)
        self.counter_max.setMinimum(0)
        self.counter_max.valueChanged.connect(self.update_counter_info)

        self.label_incr = QLabel("Increment", self.group_counters)
        self.label_incr.setGeometry(152, 30, 71, 20)
        self.counter_incr = QSpinBox(self.group_counters)
        self.counter_incr.setGeometry(128, 50, 115, 32)
        self.counter_incr.setMinimum(0)
        self.counter_incr.valueChanged.connect(self.update_counter_info)

        self.label_pos_x = QLabel("X", self.group_counters)
        self.label_pos_x.setGeometry(151, 90, 21, 18)
        self.counter_pos_x = QSpinBox(self.group_counters)
        self.counter_pos_x.setGeometry(128, 110, 55, 32)
        self.counter_pos_x.setMinimum(-1000)
        self.counter_pos_x.valueChanged.connect(self.update_counter_info)

        self.label_pox_y = QLabel("Y", self.group_counters)
        self.label_pox_y.setGeometry(210, 90, 21, 18)
        self.counter_pos_y = QSpinBox(self.group_counters)
        self.counter_pos_y.setGeometry(188, 110, 55, 32)
        self.counter_pos_y.setMinimum(-1000)
        self.counter_pos_y.valueChanged.connect(self.update_counter_info)

        self.group_extras_main = QGroupBox("Extras", self)
        self.group_extras_main.setGeometry(280, 210, 121, 191)

        self.group_extras = QGroupBox("Use Extras", self.group_extras_main)
        self.group_extras.setGeometry(10, 30, 101, 101)
        self.group_extras.setCheckable(True)
        self.group_extras.setChecked(False)
        self.group_extras.toggled.connect(self.update_extras_enabled)

        self.label_extra_index = QLabel("Extra Index", self.group_extras)
        self.label_extra_index.setGeometry(10, 31, 81, 18)
        self.extra_index = QSpinBox(self.group_extras)
        self.extra_index.setGeometry(9, 57, 81, 32)
        self.extra_index.setMinimum(0)
        self.extra_index.setMaximum(len(self.config.extras.items) - 1)
        self.extra_index.valueChanged.connect(self.update_extra_info)

        self.btn_open_extra_settings = QPushButton("Settings", self.group_extras_main)
        self.btn_open_extra_settings.setGeometry(9, 140, 103, 41)
        self.btn_open_extra_settings.pressed.connect(self.open_extra_settings)

        self.group_flags_main = QGroupBox("Flags", self)
        self.group_flags_main.setGeometry(280, 10, 121, 191)

        self.group_flags = QGroupBox("Use Flags", self.group_flags_main)
        self.group_flags.setGeometry(10, 30, 101, 101)
        self.group_flags.setCheckable(True)
        self.group_flags.setChecked(False)
        self.group_flags.toggled.connect(self.update_flags_enabled)

        self.label_flag_index = QLabel("Flag Index", self.group_flags)
        self.label_flag_index.setGeometry(10, 31, 81, 18)
        self.flag_index = QSpinBox(self.group_flags)
        self.flag_index.setGeometry(9, 57, 81, 32)
        self.flag_index.setMinimum(0)
        self.flag_index.setMaximum(len(self.config.flags) - 1)
        self.flag_index.valueChanged.connect(self.update_flag_info)

        self.btn_open_flags_settings = QPushButton("Settings", self.group_flags_main)
        self.btn_open_flags_settings.setGeometry(9, 140, 103, 41)
        self.btn_open_flags_settings.pressed.connect(self.open_flags_settings)

        self.group_bg = QGroupBox("Background Settings", self)
        self.group_bg.setGeometry(410, 360, 251, 161)

        self.label_bg_color = QLabel(f"BG Color: #{Color.pack(config.active_inv.background_color):06X}", self.group_bg)
        self.label_bg_color.setGeometry(10, 40, 161, 18)
        self.btn_bg_color = QPushButton("Set BG Color", self.group_bg)
        self.btn_bg_color.setGeometry(130, 33, 111, 32)
        self.btn_bg_color.pressed.connect(self.update_bg_color)

        self.bg_path = QLineEdit(self.group_bg)
        self.bg_path.setReadOnly(True)
        self.bg_path.setGeometry(10, 80, 231, 32)
        self.bg_path.setText(f"{config.active_inv.background}")
        self.btn_bg_open_file = QPushButton("Open File", self.group_bg)
        self.btn_bg_open_file.setGeometry(10, 117, 111, 32)
        self.btn_bg_open_file.pressed.connect(self.update_bg)

        self.group_reward = QGroupBox("Rewards", self)
        self.group_reward.setGeometry(280, 410, 121, 111)
        self.is_reward = QCheckBox("Is Reward", self.group_reward)
        self.is_reward.setGeometry(8, 30, 101, 22)
        self.is_reward.checkStateChanged.connect(self.update_rewards_enabled)
        self.btn_open_rewards_settings = QPushButton("Settings", self.group_reward)
        self.btn_open_rewards_settings.setGeometry(9, 60, 103, 41)
        self.btn_open_rewards_settings.pressed.connect(self.open_rewards_settings)

        self.group_misc = QGroupBox("Misc", self)
        self.group_misc.setGeometry(280, 530, 381, 71)
        self.btn_open_gomode_settings = QPushButton("Go Mode", self.group_misc)
        self.btn_open_gomode_settings.setGeometry(9, 30, 103, 31)
        self.btn_open_gomode_settings.pressed.connect(self.open_gomode_settings)

        self.btn_open_text_settings = QPushButton("Text Settings", self.group_misc)
        self.btn_open_text_settings.setGeometry(140, 30, 103, 31)
        self.btn_open_text_settings.pressed.connect(self.open_text_settings)

        self.btn_open_font_settings = QPushButton("Font Settings", self.group_misc)
        self.btn_open_font_settings.setGeometry(270, 30, 103, 31)
        self.btn_open_font_settings.pressed.connect(self.open_font_settings)

        self.btn_save_cfg = QPushButton("Save Config", self)
        self.btn_save_cfg.setGeometry(900, 568, 101, 34)
        self.btn_save_cfg.pressed.connect(self.save_config)

        self.selection_changed()
        self.setFixedSize(1012, 610)
        self.setWindowTitle("Tracker Editor")
        self.setWindowIcon(self.tracker.windowIcon())

        # start centered
        qtRectangle = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.show()

    def get_item(self):
        return self.config.active_inv.items[self.list_selected.currentIndex().row()]

    def clear_item_flags(self, item: InventoryItem):
        for pixmap_item in item.pixmap_items:
            pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

            pixmap_item.state.infos.img_index = -1
            if pixmap_item.flag is not None and item.flag_index is not None:
                pixmap_item.state.infos.flag_text_index = 0
                pixmap_item.update_flag(True)
            pixmap_item.update_item_visibility()

    def clear_prev_item_flags(self):
        if self.prev_item is not None:
            self.clear_item_flags(self.prev_item)

    def change_item_flags(self, index: int, do_prev_clear: bool):
        item = self.get_item()

        self.clear_item_flags(item)

        if do_prev_clear:
            self.clear_prev_item_flags()

        item.pixmap_items[index].setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        item.pixmap_items[index].setSelected(True)

        item.pixmap_items[index].state.infos.img_index = 0
        if item.pixmap_items[index].flag is not None and item.flag_index is not None:
            item.pixmap_items[index].state.infos.flag_text_index = 1
            item.pixmap_items[index].update_flag(True)
        item.pixmap_items[index].update_item_visibility()

    def selection_changed(self):
        item = self.get_item()

        # update item name line edit
        self.item_name.setText(item.name)

        # update position/angle table
        self.pause_update = True
        index = self.item_pos_index.value() - 1
        self.group_pos_settings.setTitle(f"Position Settings ({index + 1} / {len(item.positions)})")
        self.item_pos_index.setMaximum(len(item.positions))
        self.item_pos_index.setValue(self.item_pos_index.minimum())
        self.pos_x.setValue(item.positions[index].x)
        self.pos_y.setValue(item.positions[index].y)
        self.angle.setValue(int(item.pixmap_items[index].rotation()))

        # update sources listview
        self.model_cache_sources.clear()
        for src_item in item.sources:
            self.model_cache_sources.append((True, str(src_item.path), QPixmap(str(src_item.path))))
        self.list_sources.model().deleteLater()
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()
        self.model_sources.currentChanged.connect(
            self.sources_selection_update
        )  # TODO: figure out if this is necessary
        self.sources_selection_update()

        # update counters table
        self.group_counters.setChecked(item.counter is not None)
        if item.counter is not None:
            self.counter_text_index.setValue(item.counter.text_settings_index)
            self.counter_min.setValue(item.counter.min)
            self.counter_max.setValue(item.counter.max)
            self.counter_incr.setValue(item.counter.increment)
            self.counter_pos_x.setValue(item.counter.pos.x)
            self.counter_pos_y.setValue(item.counter.pos.y)

            item.counter.show = True
            for pixmap_item in item.pixmap_items:
                pixmap_item.label_counter.setVisible(True)
        else:
            self.counter_text_index.setValue(0)
            self.counter_min.setValue(0)
            self.counter_max.setValue(0)
            self.counter_incr.setValue(0)
            self.counter_pos_x.setValue(0)
            self.counter_pos_y.setValue(0)

        # update extras group
        self.group_extras.setChecked(item.extra_index is not None)
        if item.extra_index is not None:
            self.extra_index.setValue(item.extra_index)

        # update flags group
        self.group_flags.setChecked(item.flag_index is not None)
        if item.flag_index is not None:
            self.flag_index.setValue(item.flag_index)

        # update rewards
        self.is_reward.setChecked(item.is_reward)

        def toggle_all(target_item: InventoryItem, enabled: bool):
            for pixmap_item in target_item.pixmap_items:
                if target_item.counter is not None:
                    pixmap_item.label_counter.setVisible(enabled)

                if pixmap_item.extra is not None:
                    pixmap_item.extra.setVisible(enabled)

                if pixmap_item.flag is not None:
                    pixmap_item.flag.setVisible(enabled)

        toggle_all(item, True)
        if self.prev_item is not None:
            toggle_all(self.prev_item, False)

        self.change_item_flags(0, True)
        self.prev_item = item
        self.pause_update = False

    def item_pos_value_changed(self, value: int):
        if self.pause_update:
            return

        item = self.get_item()
        self.group_pos_settings.setTitle(f"Position Settings ({value} / {len(item.positions)})")
        self.pos_x.setValue(item.positions[value - 1].x)
        self.pos_y.setValue(item.positions[value - 1].y)
        self.angle.setValue(int(item.pixmap_items[value - 1].rotation()))
        self.change_item_flags(value - 1, False)

    def item_pos_add(self):
        self.pause_update = True
        item = self.get_item()
        index = len(item.positions)
        item.positions.append(Pos(0, 0))
        self.item_pos_index.setMaximum(len(item.positions))
        self.item_pos_index.setValue(index + 1)
        self.tracker.create_item(item, index, item.positions[-1])
        self.pause_update = False
        self.item_pos_value_changed(index + 1)

    def item_pos_del(self):
        item = self.get_item()
        index = self.item_pos_index.value() - 1
        item.positions.pop(index)
        self.item_pos_index.setMaximum(len(item.positions))
        self.item_pos_index.setValue(index)
        self.tracker.scene.removeItem(item.pixmap_items[index])

    def update_item_surroundings(self, index: int):
        offset = self.tracker.get_item_os_offset()
        item = self.get_item()

        if item.counter is not None and item.pixmap_items[index].label_counter is not None:
            pos = Pos(item.positions[index].x + offset, item.positions[index].y + offset)
            pos.x += item.counter.pos.x
            pos.y += item.counter.pos.y
            item.pixmap_items[index].label_counter.setPos(float(pos.x), float(pos.y))

        if item.flag_index is not None and item.pixmap_items[index].flag is not None:
            flag = self.config.flags[item.flag_index]
            pos = Pos(item.positions[index].x + offset, item.positions[index].y + offset)
            pos.x += flag.pos.x
            pos.y += flag.pos.y
            item.pixmap_items[index].flag.setPos(float(pos.x), float(pos.y))

        if item.extra_index is not None and item.pixmap_items[index].extra is not None:
            extra = self.config.extras.items[item.extra_index]
            pos = Pos(item.positions[index].x + offset, item.positions[index].y + offset)
            pos.x += extra.pos.x
            pos.y += extra.pos.y
            item.pixmap_items[index].extra.setPos(float(pos.x), float(pos.y))

        if item.is_reward and index in item.reward_map:
            reward_info = self.config.active_inv.rewards.items[item.pixmap_items[index].state.infos.reward_index]
            pos = Pos(item.positions[index].x + offset, item.positions[index].y + offset)
            pos.x += reward_info.pos.x
            pos.y += reward_info.pos.y
            item.reward_map[index].setPos(float(pos.x), float(pos.y))

    def update_pos_x(self, value: int):
        if self.pause_update:
            return

        index = self.item_pos_index.value() - 1
        item = self.get_item()
        item.pixmap_items[index].setPos(value, self.pos_y.value())
        item.positions[index].x = value
        self.update_item_surroundings(index)

    def update_pos_y(self, value: int):
        if self.pause_update:
            return

        index = self.item_pos_index.value() - 1
        item = self.get_item()
        item.pixmap_items[index].setPos(self.pos_x.value(), value)
        item.positions[index].y = value
        self.update_item_surroundings(index)

    def update_pos(self, new_pos: QPoint):
        # called when we're dragging the item with the mouse
        index = self.item_pos_index.value() - 1
        item = self.get_item()
        self.pause_update = True
        self.pos_x.setValue(new_pos.x())
        self.pos_y.setValue(new_pos.y())
        item.positions[index].x = new_pos.x()
        item.positions[index].y = new_pos.y()
        self.pause_update = False
        self.update_item_surroundings(index)

    def update_angle(self, value: int):
        if self.pause_update:
            return

        item = self.get_item()
        item.pixmap_items[self.item_pos_index.value() - 1].setRotation(value)
        item.rotation = value

    def save_config(self):
        self.config.to_xml()
        print("Config saved successfully!")

    def add_item(self):
        pass

    def remove_item(self):
        item = self.get_item()
        scene = item.pixmap_items[0].scene()

        if scene is not None:
            self.model_cache.pop(item.index)
            self.config.active_inv.remove_item(item.index)

            if item.pixmap_items[0].label_counter is not None:
                scene.removeItem(item.pixmap_items[0].label_counter)

            scene.removeItem(item.pixmap_items[0])
            self.list_selected.viewport().update()

    def update_item_name(self):
        item = self.get_item()
        item.name = self.item_name.text()

        index = self.list_selected.currentIndex().row()
        model_item = self.model_cache[index]
        model_item = (model_item[0], item.name, model_item[2])
        self.model_cache[index] = model_item
        self.list_selected.viewport().update()

    def update_counter_info(self, new_value: int):
        if self.pause_update:
            return

        item = self.get_item()

        if item.counter is None:
            item.counter = Counter(
                self.counter_min.value(),
                self.counter_max.value(),
                self.counter_incr.value(),
                0,  # TODO
                self.counter_text_index.value(),
                Pos(self.counter_pos_x.value(), self.counter_pos_y.value()),
                False,  # TODO
            )
        else:
            item.counter.min = self.counter_min.value()
            item.counter.max = self.counter_max.value()
            item.counter.increment = self.counter_incr.value()
            item.counter.middle_click_increment = 0  # TODO
            item.counter.text_settings_index = self.counter_text_index.value()
            item.counter.pos.x = self.counter_pos_x.value()
            item.counter.pos.y = self.counter_pos_y.value()
            item.counter.use_wheel = False  # TODO

        item.counter.value = item.counter.min

        for pixmap_item in item.pixmap_items:
            pos = pixmap_item.pos()
            pixmap_item.label_counter.setPos(pos.x() + item.counter.pos.x, pos.y() + item.counter.pos.y)
            pixmap_item.label_counter.set_text_style(item.counter.text_settings_index, False)
            pixmap_item.label_counter.set_max_width(f"{item.counter.max}")

    def update_counter_enabled(self, enabled: bool):
        if self.pause_update:
            return

        item = self.get_item()

        for pixmap_item in item.pixmap_items:
            pixmap_item.label_counter.setVisible(enabled)

        if enabled:
            self.update_counter_info(0)
        else:
            item.counter = None

        if item.counter is not None:
            item.counter.show = enabled

    def update_bg_color(self):
        picked_qcolor = QColorDialog.getColor(
            Color.convert(self.config.active_inv.background_color), self, "Tracker Background Color Picker"
        )
        self.config.active_inv.background_color.r = picked_qcolor.red()
        self.config.active_inv.background_color.g = picked_qcolor.green()
        self.config.active_inv.background_color.b = picked_qcolor.blue()
        self.label_bg_color.setText(f"BG Color: #{Color.pack(self.config.active_inv.background_color):06X}")
        self.tracker.view.setStyleSheet(
            f"background-color: {Color.to_css(self.config.active_inv.background_color)}; border: 0px;"
        )

    def update_bg(self):
        config_folder = self.config.config_path.parent
        path_str = QFileDialog.getOpenFileName(self, "Open Background Image", str(config_folder), "*.png")[0]

        if len(path_str) == 0:
            print("operation was cancelled (bg img file open)")
            return

        # resolve path, make sure it exists and copy the file to the config folder if the path isn't relative to it
        path = Path(path_str).resolve()
        assert path.exists(), "background path doesn't exist?"
        path = move_file_to_config(self.config, path)

        # update the config, the ui and the window
        self.config.active_inv.background = path
        self.bg_path.setText(str(path))
        self.tracker.update_window()

    def update_extra_info(self, new_value: int):
        item = self.get_item()
        item.extra_index = new_value
        offset = self.tracker.get_item_os_offset()

        for i, pixmap_item in enumerate(item.pixmap_items):
            pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)

            if item.pixmap_items[i].extra is not None:
                self.tracker.scene.removeItem(item.pixmap_items[i].extra)

            self.tracker.create_extra(item, i, pixmap_item.obj_name, pos)
            item.pixmap_items[i].extra.setVisible(True)

    def update_extras_enabled(self, enabled: bool):
        item = self.get_item()

        if enabled:
            item.extra_index = self.extra_index.value()
        else:
            item.extra_index = None

        for pixmap_item in item.pixmap_items:
            if pixmap_item.extra is not None:
                pixmap_item.extra.setVisible(enabled)

    def update_flag_info(self, new_value: int):
        item = self.get_item()
        item.flag_index = new_value
        offset = self.tracker.get_item_os_offset()

        for i, pixmap_item in enumerate(item.pixmap_items):
            pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)

            if item.pixmap_items[i].flag is None:
                self.tracker.create_flag(item, i, pixmap_item.obj_name, pos)

            pixmap_item.update_flag()

    def update_flags_enabled(self, enabled: bool):
        item = self.get_item()

        if enabled:
            if item.flag_index is None:
                item.flag_index = self.flag_index.value()
        else:
            item.flag_index = None

        if item.flag_index is not None:
            for pixmap_item in item.pixmap_items:
                if pixmap_item.flag is not None:
                    pixmap_item.flag.setVisible(enabled)

                if enabled:
                    pixmap_item.update_flag()

    def update_rewards_enabled(self, state):
        item = self.get_item()

        if self.pause_update:
            return

        offset = self.tracker.get_item_os_offset()
        enabled = self.is_reward.isChecked()

        item.is_reward = enabled
        for i, pixmap_item in enumerate(item.pixmap_items):
            if i not in item.reward_map:
                pos = Pos(item.positions[i].x + offset, item.positions[i].y + offset)
                self.tracker.create_reward(item, i, pixmap_item.obj_name, pos)

            item.reward_map[i].setVisible(enabled)

        # rewards and extras can't co-exist
        self.group_extras.setEnabled(not enabled)
        if enabled:
            self.group_extras.setChecked(False)

    def sources_add(self):
        item = self.get_item()
        src_dir = item.sources[0].path.parent

        paths_str = QFileDialog.getOpenFileNames(self, "Open Item Icon", str(src_dir), "*.png")[0]

        if len(paths_str) == 0:
            print("operation cancelled (source files open)")
            return

        for path_str in paths_str:
            path = Path(path_str).resolve()
            assert path.exists(), "path doesn't exist?"
            path = move_file_to_config(self.config, path)

            item.sources.append(SourceItem(path.stem, path))
            self.model_cache_sources.append((True, str(path), QPixmap(str(path))))
        self.list_sources.viewport().update()

        for pixmap_item in item.pixmap_items:
            pixmap_item.update_item_visibility()

    def sources_del(self):
        item = self.get_item()
        index = self.list_sources.currentIndex().row()

        # TODO: figure this out
        if index + 1 == len(item.sources):
            print("TODO: unknown issue with last entry, aborting")
            return

        if index >= 0:
            item.sources.pop(index)
            self.model_cache_sources.pop(index)
            self.list_sources.setCurrentIndex(self.list_sources.model().index(index - 1, 0))
            self.list_sources.viewport().update()

            for pixmap_item in item.pixmap_items:
                pixmap_item.update_item_visibility()

    def sources_open(self):
        item = self.get_item()
        index = self.list_sources.currentIndex().row()
        src_dir = item.sources[index].path.parent

        if index < 0:
            return

        path_str = QFileDialog.getOpenFileName(self, "Open Item Icon", str(src_dir), "*.png")[0]

        if len(path_str) == 0:
            print("operation cancelled (source file open)")
            return

        path = Path(path_str).resolve()
        assert path.exists(), "path doesn't exist?"
        path = move_file_to_config(self.config, path)

        item.sources[index].name = path.stem
        item.sources[index].path = path
        self.model_cache_sources[index] = (True, str(path), QPixmap(str(path)))
        self.list_sources.viewport().update()

    def sources_move_up(self):
        item = self.get_item()
        index = self.list_sources.currentIndex().row()

        if index - 1 >= 0:
            prev_elem = self.model_cache_sources[index - 1]
            cur_elem = self.model_cache_sources[index]
            self.model_cache_sources[index] = prev_elem
            self.model_cache_sources[index - 1] = cur_elem
            self.list_sources.viewport().update()

        if index - 1 >= 0:
            prev_elem = item.sources[index - 1]
            cur_elem = item.sources[index]
            item.sources[index] = prev_elem
            item.sources[index - 1] = cur_elem

        for pixmap_item in item.pixmap_items:
            pixmap_item.update_item_visibility()

        self.sources_selection_update()

    def sources_move_down(self):
        item = self.get_item()
        index = self.list_sources.currentIndex().row()

        if index + 1 < len(self.model_cache_sources):
            cur_elem = self.model_cache_sources[index]
            next_elem = self.model_cache_sources[index + 1]
            self.model_cache_sources[index] = next_elem
            self.model_cache_sources[index + 1] = cur_elem
            self.list_sources.viewport().update()

        if index + 1 < len(item.sources):
            cur_elem = item.sources[index]
            next_elem = item.sources[index + 1]
            item.sources[index] = next_elem
            item.sources[index + 1] = cur_elem

        for pixmap_item in item.pixmap_items:
            pixmap_item.update_item_visibility()

        self.sources_selection_update()

    def sources_selection_update(self):
        index = self.list_sources.currentIndex().row()
        self.btn_sources_del.setEnabled(len(self.model_cache_sources) > 1)
        self.btn_sources_up.setEnabled(index - 1 >= 0)
        self.btn_sources_down.setEnabled(index + 1 < len(self.model_cache_sources))

    def open_text_settings(self):
        dialog = TextSettingsDialog(self.config, self)
        dialog.open()

    def open_gomode_settings(self):
        dialog = GoModeSettingsDialog(self.config, self)
        dialog.open()

    def open_rewards_settings(self):
        dialog = RewardSettingsDialog(self.config, self)
        dialog.open()

    def open_extra_settings(self):
        dialog = ExtraSettingsDialog(self.config, self)
        dialog.open()

    def open_flags_settings(self):
        dialog = FlagSettingsDialog(self.config, self)
        dialog.open()

    def open_font_settings(self):
        dialog = FontSettingsDialog(self.config, self)
        dialog.open()


class TrackerEditor(TrackerWindow):
    def __init__(self, parent: Optional[QWidget], configs: dict[Path, Config], config_index: int):
        super().__init__(parent, configs, config_index, True)

        self.edit_menu = TrackerEditorMenu(self.config, self)
        self.config.edit_menu = self.edit_menu
        self.config.edit_menu.list_selected.clearSelection()

    def closeEvent(self, e):
        self.edit_menu.close()
        self.config.edit_menu = None
        super().closeEvent(e)

    def update_window(self):
        if self.config.edit_menu is not None:
            self.config.edit_menu.clear_prev_item_flags()
            super().update_window()

            self.config.edit_menu = self.edit_menu
            self.config.edit_menu.config = self.config
            self.config.edit_menu.prev_item = None
            self.config.edit_menu.list_selected.clearSelection()
