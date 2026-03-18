from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QGuiApplication, QPixmap
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
)

from common import ListViewModel, Color, Pos
from config import Config, InventoryItem, Counter
from shutil import copyfile
from tracker import TrackerWindow


class TrackerEditorMenu(QWidget):
    def __init__(self, config: Config, tracker: "TrackerEditor"):
        super().__init__()
        self.config = config
        self.tracker = tracker
        self.prev_item: Optional[InventoryItem] = None
        self.do_counter_value_changed = True  # TODO: find something better

        first_item = self.config.active_inv.items[0]

        # items section
        self.label_selected_items = QLabel("Items", self)
        self.label_selected_items.setGeometry(10, 10, 70, 20)
        self.list_selected = QListView(self)
        self.list_selected.setGeometry(10, 30, 240, 570)

        self.model_cache: list[tuple[bool, str, QPixmap]] = []
        for item in self.config.active_inv.items:
            self.model_cache.append((True, item.name, item.pixmap_items[0].pixmap().scaled(32, 32)))
        self.list_selected.setModel(ListViewModel(self.model_cache))
        self.list_selected.setCurrentIndex(self.list_selected.model().index(0, 0))
        self.model = self.list_selected.selectionModel()
        self.model.currentChanged.connect(self.selection_changed)

        # item name, paths and sources section
        self.label_item_name = QLabel("Item Name", self)
        self.label_item_name.setGeometry(260, 10, 70, 20)
        self.item_name = QLineEdit(self)
        self.item_name.setGeometry(260 - 1, 30, 250 + 2, 30 + 2)
        self.item_name.textChanged.connect(self.update_item_name)

        self.group_pos = QGroupBox("Positions", self)
        self.group_pos.setGeometry(260, 70, 251, 371)

        self.table_pos = QTableWidget(self.group_pos)
        self.table_pos.setGeometry(10, 30, 231, 301)
        self.table_pos.setColumnCount(3)
        self.table_pos.setHorizontalHeaderItem(0, QTableWidgetItem("X"))
        self.table_pos.setHorizontalHeaderItem(1, QTableWidgetItem("Y"))
        self.table_pos.setHorizontalHeaderItem(2, QTableWidgetItem("Angle"))
        self.table_pos.horizontalHeader().setDefaultSectionSize(60)
        self.table_pos.setRowCount(len(first_item.positions))
        self.table_pos.itemSelectionChanged.connect(self.update_tracker_selection)
        self.table_pos.itemDelegate().closeEditor.connect(self.update_tracker_pos)

        for i, pos in enumerate(first_item.positions):
            self.table_pos.setVerticalHeaderItem(i, QTableWidgetItem(f"Pos. {i + 1}"))
            self.table_pos.setItem(i, 0, QTableWidgetItem(f"{pos.x}"))
            self.table_pos.setItem(i, 1, QTableWidgetItem(f"{pos.y}"))
            self.table_pos.setItem(i, 2, QTableWidgetItem("0.0"))

        self.btn_table_pos_add = QPushButton("Add", self.group_pos)
        self.btn_table_pos_add.setGeometry(9, 340, 111, 21)
        self.btn_table_pos_add.pressed.connect(self.table_pos_add)
        self.btn_table_pos_del = QPushButton("Remove", self.group_pos)
        self.btn_table_pos_del.setGeometry(130, 340, 111, 21)
        self.btn_table_pos_del.pressed.connect(self.table_pos_del)

        self.group_sources = QGroupBox("Icon Paths", self)
        self.group_sources.setGeometry(520, 30, 521, 301)

        self.list_sources = QListView(self.group_sources)
        self.list_sources.setGeometry(10, 30, 501, 241)

        self.model_cache_sources: list[tuple[bool, str, QPixmap]] = []
        for src_item in first_item.sources:
            self.model_cache_sources.append((True, str(src_item.path), QPixmap(str(src_item.path))))
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()
        # self.model_sources.currentChanged.connect(self.selection_changed)

        self.btn_sources_add = QPushButton("Add", self.group_sources)
        self.btn_sources_add.setGeometry(9, 275, 71, 21)
        self.btn_sources_del = QPushButton("Remove", self.group_sources)
        self.btn_sources_del.setGeometry(89, 275, 71, 21)
        self.btn_sources_open = QPushButton("Open File", self.group_sources)
        self.btn_sources_open.setGeometry(170, 275, 71, 21)

        self.group_counters = QGroupBox("Use Counters", self)
        self.group_counters.setGeometry(260, 450, 251, 151)
        self.group_counters.setCheckable(True)
        self.group_counters.setChecked(False)
        self.group_counters.toggled.connect(self.update_counter_enabled)

        self.label_text_index = QLabel("Text Set.", self.group_counters)
        self.label_text_index.setGeometry(10, 30, 61, 18)
        self.counter_text_index = QSpinBox(self.group_counters)
        self.counter_text_index.setGeometry(8, 50, 55, 32)
        self.counter_text_index.setMinimum(0)
        self.counter_text_index.setMaximum(len(self.config.text_settings) - 1)
        self.counter_text_index.valueChanged.connect(self.update_counter_info)

        self.label_min = QLabel("Min.", self.group_counters)
        self.label_min.setGeometry(82, 30, 31, 18)
        self.counter_min = QSpinBox(self.group_counters)
        self.counter_min.setGeometry(68, 50, 55, 32)
        self.counter_min.setMinimum(0)
        self.counter_min.valueChanged.connect(self.update_counter_info)

        self.label_max = QLabel("Max.", self.group_counters)
        self.label_max.setGeometry(139, 30, 41, 18)
        self.counter_max = QSpinBox(self.group_counters)
        self.counter_max.setGeometry(128, 50, 55, 32)
        self.counter_max.setMinimum(0)
        self.counter_max.valueChanged.connect(self.update_counter_info)

        self.label_incr = QLabel("Incr.", self.group_counters)
        self.label_incr.setGeometry(202, 30, 31, 18)
        self.counter_incr = QSpinBox(self.group_counters)
        self.counter_incr.setGeometry(188, 50, 55, 32)
        self.counter_incr.setMinimum(0)
        self.counter_incr.valueChanged.connect(self.update_counter_info)

        self.label_pos_x = QLabel("X", self.group_counters)
        self.label_pos_x.setGeometry(31, 90, 21, 18)
        self.counter_pos_x = QSpinBox(self.group_counters)
        self.counter_pos_x.setGeometry(8, 110, 55, 32)
        self.counter_pos_x.setMinimum(-1000)
        self.counter_pos_x.valueChanged.connect(self.update_counter_info)

        self.label_pox_y = QLabel("Y", self.group_counters)
        self.label_pox_y.setGeometry(90, 90, 21, 18)
        self.counter_pox_y = QSpinBox(self.group_counters)
        self.counter_pox_y.setGeometry(68, 110, 55, 32)
        self.counter_pox_y.setMinimum(-1000)
        self.counter_pox_y.valueChanged.connect(self.update_counter_info)

        self.label_width = QLabel("Width", self.group_counters)
        self.label_width.setGeometry(135, 90, 41, 18)
        self.counter_width = QSpinBox(self.group_counters)
        self.counter_width.setGeometry(128, 110, 55, 32)
        self.counter_width.setMinimum(0)
        self.counter_width.valueChanged.connect(self.update_counter_info)

        self.label_height = QLabel("Height", self.group_counters)
        self.label_height.setGeometry(193, 90, 51, 18)
        self.counter_height = QSpinBox(self.group_counters)
        self.counter_height.setGeometry(188, 110, 55, 32)
        self.counter_height.setMinimum(0)
        self.counter_height.valueChanged.connect(self.update_counter_info)

        self.btn_counters_add = QPushButton("Add", self.group_counters)
        self.btn_counters_add.setGeometry(9, 274, 111, 21)
        self.btn_counters_del = QPushButton("Remove", self.group_counters)
        self.btn_counters_del.setGeometry(130, 274, 111, 21)

        self.group_rewards = QGroupBox("Use Rewards", self)
        self.group_rewards.setGeometry(520, 340, 521, 261)
        self.group_rewards.setCheckable(True)
        self.group_rewards.setChecked(False)
        self.group_rewards.toggled.connect(self.update_rewards_enabled)

        self.table_rewards = QTableWidget(self.group_rewards)
        self.table_rewards.setGeometry(10, 30, 501, 201)
        self.table_rewards.setColumnCount(len(config.active_inv.rewards.items))
        self.table_rewards.setHorizontalHeaderItem(0, QTableWidgetItem("Reward 1"))
        self.table_rewards.setRowCount(5)
        self.table_rewards.setVerticalHeaderItem(0, QTableWidgetItem("Text Settings Index"))
        self.table_rewards.setVerticalHeaderItem(1, QTableWidgetItem("Name"))
        self.table_rewards.setVerticalHeaderItem(2, QTableWidgetItem("Position (rel.)"))
        self.table_rewards.setVerticalHeaderItem(3, QTableWidgetItem("Width"))
        self.table_rewards.setVerticalHeaderItem(4, QTableWidgetItem("Height"))

        for i, reward_item in enumerate(config.active_inv.rewards.items):
            self.table_rewards.setItem(0, i, QTableWidgetItem(f"{reward_item.text_settings_index}"))
            self.table_rewards.setItem(1, i, QTableWidgetItem(f"{reward_item.name}"))
            self.table_rewards.setItem(2, i, QTableWidgetItem(f"{reward_item.pos.x};{reward_item.pos.y}"))
            self.table_rewards.setItem(3, i, QTableWidgetItem(f"{reward_item.width}"))
            self.table_rewards.setItem(4, i, QTableWidgetItem(f"{reward_item.height}"))

        self.btn_rewards_add = QPushButton("Add", self.group_rewards)
        self.btn_rewards_add.setGeometry(9, 233, 111, 21)
        self.btn_rewards_del = QPushButton("Remove", self.group_rewards)
        self.btn_rewards_del.setGeometry(130, 233, 111, 21)

        self.group_extras = QGroupBox("Use Extras", self)
        self.group_extras.setGeometry(520, 610, 101, 101)
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

        self.group_flags = QGroupBox("Use Flags", self)
        self.group_flags.setGeometry(630, 610, 101, 101)
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

        self.group_bg = QGroupBox("Background Settings", self)
        self.group_bg.setGeometry(740, 610, 301, 101)

        self.label_bg_color = QLabel(f"BG Color: #{Color.pack(config.active_inv.background_color):06X}", self.group_bg)
        self.label_bg_color.setGeometry(10, 37, 161, 18)
        self.btn_bg_color = QPushButton("Set BG Color", self.group_bg)
        self.btn_bg_color.setGeometry(183, 30, 111, 32)
        self.btn_bg_color.pressed.connect(self.update_bg_color)

        self.bg_path = QLineEdit(self.group_bg)
        self.bg_path.setReadOnly(True)
        self.bg_path.setGeometry(9, 65, 171, 32)
        self.bg_path.setText(f"{config.active_inv.background}")
        self.btn_bg_open_file = QPushButton("Open File", self.group_bg)
        self.btn_bg_open_file.setGeometry(183, 65, 111, 32)
        self.btn_bg_open_file.pressed.connect(self.update_bg)

        self.btn_add_item = QPushButton("Add Item", self)
        self.btn_add_item.setGeometry(10, 605, 111, 34)
        self.btn_add_item.pressed.connect(self.add_item)

        self.btn_delete_item = QPushButton("Delete Item", self)
        self.btn_delete_item.setGeometry(140, 605, 111, 34)
        self.btn_delete_item.pressed.connect(self.remove_item)

        self.separator_1 = QFrame(self)
        self.separator_1.setGeometry(10, 660, 500, 20)
        self.separator_1.setFrameShape(QFrame.Shape.HLine)
        self.separator_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.btn_save_cfg = QPushButton("Save Config", self)
        self.btn_save_cfg.setGeometry(10, 678, 111, 34)
        self.btn_save_cfg.pressed.connect(self.save_config)

        # ---

        # self.label_angle = QLabel("Angle", self)
        # self.label_angle.setGeometry(368, 30, 41, 20)
        # self.angle = QSpinBox(self)
        # self.angle.setGeometry(360, 50, 50, 30)
        # self.angle.setMaximum(360)
        # self.angle.valueChanged.connect(self.update_angle)

        # ---

        # self.selection_changed()
        self.setGeometry(0, 0, 1050, 720)
        self.setFixedSize(1050, 720)
        self.setWindowTitle("Tracker Editor")

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
                pixmap_item.update_flag()
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
            item.pixmap_items[index].update_flag()
        item.pixmap_items[index].update_item_visibility()

    def selection_changed(self):
        item = self.get_item()

        # update item name line edit
        self.item_name.setText(item.name)

        # update position/angle table
        self.table_pos.setRowCount(len(item.positions))
        for i, pos in enumerate(item.positions):
            if self.table_pos.verticalHeaderItem(i) is None:
                self.table_pos.setVerticalHeaderItem(i, QTableWidgetItem(f"Pos. {i + 1}"))

            table_item = self.table_pos.item(i, 0)
            if table_item is not None:
                table_item.setText(f"{pos.x}")
            else:
                self.table_pos.setItem(i, 0, QTableWidgetItem(f"{pos.x}"))

            table_item = self.table_pos.item(i, 1)
            if table_item is not None:
                table_item.setText(f"{pos.y}")
            else:
                self.table_pos.setItem(i, 1, QTableWidgetItem(f"{pos.y}"))

            table_item = self.table_pos.item(i, 2)
            if table_item is not None:
                table_item.setText(f"{item.pixmap_items[0].rotation()}")
            else:
                self.table_pos.setItem(i, 2, QTableWidgetItem(f"{item.pixmap_items[0].rotation()}"))

        # update sources listview
        self.model_cache_sources.clear()
        for src_item in item.sources:
            self.model_cache_sources.append((True, str(src_item.path), QPixmap(str(src_item.path))))
        self.list_sources.model().deleteLater()
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()

        # update counters table
        self.do_counter_value_changed = False
        self.group_counters.setChecked(item.counter is not None)
        if item.counter is not None:
            self.counter_text_index.setValue(item.counter.text_settings_index)
            self.counter_min.setValue(item.counter.min)
            self.counter_max.setValue(item.counter.max)
            self.counter_incr.setValue(item.counter.increment)
            self.counter_pos_x.setValue(item.counter.pos.x)
            self.counter_pox_y.setValue(item.counter.pos.y)
            self.counter_width.setValue(item.counter.width)
            self.counter_height.setValue(item.counter.height)

            item.counter.show = True
            for pixmap_item in item.pixmap_items:
                pixmap_item.label_counter.setVisible(True)
        else:
            self.counter_text_index.setValue(0)
            self.counter_min.setValue(0)
            self.counter_max.setValue(0)
            self.counter_incr.setValue(0)
            self.counter_pos_x.setValue(0)
            self.counter_pox_y.setValue(0)
            self.counter_width.setValue(0)
            self.counter_height.setValue(0)
        self.do_counter_value_changed = True

        # update rewards
        self.group_rewards.setChecked(item.is_reward)

        # update extras group
        self.group_extras.setChecked(item.extra_index is not None)
        if item.extra_index is not None:
            self.extra_index.setValue(item.extra_index)

        # update flags group
        self.group_flags.setChecked(item.flag_index is not None)
        if item.flag_index is not None:
            self.flag_index.setValue(item.flag_index)

        self.change_item_flags(0, True)
        self.prev_item = item

    def update_pos(self, new_pos: QPoint):
        cur_index = self.table_pos.currentIndex().row()

        if cur_index < 0:
            cur_index = 0

        item_x = self.table_pos.item(cur_index, 0)
        item_y = self.table_pos.item(cur_index, 1)
        assert item_x is not None
        assert item_y is not None
        item_x.setText(str(new_pos.x()))
        item_y.setText(str(new_pos.y()))

    def update_angle(self, value: int):
        item = self.get_item()
        item.pixmap_items[0].setRotation(value)
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
        self.list_selected.update(self.list_selected.currentIndex())

    def update_tracker_pos(self, widget: QWidget, hint):
        cur_index = self.table_pos.currentIndex().row()
        item_x = self.table_pos.item(cur_index, 0)
        item_y = self.table_pos.item(cur_index, 1)
        assert item_x is not None
        assert item_y is not None

        pos_x = int(item_x.text())
        pos_y = int(item_y.text())
        item = self.get_item()
        item.pixmap_items[cur_index].setPos(pos_x, pos_y)
        item.positions[cur_index].x = pos_x
        item.positions[cur_index].y = pos_y

    def update_tracker_selection(self):
        self.change_item_flags(self.table_pos.currentIndex().row(), False)

    def table_pos_add(self):
        item = self.get_item()
        index = len(item.positions)
        self.table_pos.setRowCount(index + 1)
        self.table_pos.setVerticalHeaderItem(index, QTableWidgetItem(f"Pos. {index + 1}"))
        self.table_pos.setItem(index, 0, QTableWidgetItem("0"))
        self.table_pos.setItem(index, 1, QTableWidgetItem("0"))
        self.table_pos.setItem(index, 2, QTableWidgetItem("0.0"))

        item.positions.append(Pos(0, 0))
        self.tracker.create_item(item, index, item.positions[-1])

    def table_pos_del(self):
        cur_index = self.table_pos.currentIndex().row()

        if cur_index > 0:
            item = self.get_item()
            self.table_pos.removeRow(cur_index)
            self.tracker.scene.removeItem(item.pixmap_items[cur_index])
            item.pixmap_items.pop(cur_index)
            item.positions.pop(cur_index)
            self.table_pos.selectRow(cur_index - 1)
        else:
            print("won't remove because index is 0")

    def update_counter_info(self, new_value: int):
        if not self.do_counter_value_changed:
            return

        item = self.get_item()

        if item.counter is None:
            item.counter = Counter(
                self.counter_min.value(),
                self.counter_max.value(),
                self.counter_incr.value(),
                0,  # TODO
                self.counter_text_index.value(),
                Pos(self.counter_pos_x.value(), self.counter_pox_y.value()),
                self.counter_width.value(),
                self.counter_height.value(),
                False,  # TODO
            )
        else:
            item.counter.min = self.counter_min.value()
            item.counter.max = self.counter_max.value()
            item.counter.increment = self.counter_incr.value()
            item.counter.middle_click_increment = 0  # TODO
            item.counter.text_settings_index = self.counter_text_index.value()
            item.counter.pos.x = self.counter_pos_x.value()
            item.counter.pos.y = self.counter_pox_y.value()
            item.counter.width = self.counter_width.value()
            item.counter.height = self.counter_height.value()
            item.counter.use_wheel = False  # TODO

        item.counter.value = item.counter.min

        for pixmap_item in item.pixmap_items:
            pos = pixmap_item.pos()
            pixmap_item.label_counter.setPos(pos.x() + item.counter.pos.x, pos.y() + item.counter.pos.y)
            pixmap_item.label_counter.set_text_style(item.counter.text_settings_index, False)
            pixmap_item.label_counter.set_max_width(f"{item.counter.max}")

    def update_counter_enabled(self, enabled: bool):
        if not self.do_counter_value_changed:
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
        if not path.is_relative_to(config_folder):
            dest = config_folder / f"{path.stem}{path.suffix}"
            copyfile(path, dest)
            path = dest

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

            if item.pixmap_items[i].extra is None:
                self.tracker.create_extra(item, i, pixmap_item.obj_name, pos)

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
            item.flag_index = self.flag_index.value()
        else:
            item.flag_index = None

        if item.flag_index is not None:
            for pixmap_item in item.pixmap_items:
                pixmap_item.flag.setVisible(enabled)

                if enabled:
                    pixmap_item.update_flag()

    def update_rewards_enabled(self, enabled: bool):
        # rewards and extras can't co-exist
        self.group_extras.setEnabled(not enabled)

        if enabled:
            self.group_extras.setChecked(False)


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
