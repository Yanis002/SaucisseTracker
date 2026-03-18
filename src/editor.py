from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QListView, QPushButton, QSpinBox, QGraphicsItem, QFrame, QLineEdit, QGroupBox, QTableWidget, QTableWidgetItem

from common import ListViewModel, Color
from config import Config, InventoryItem
from tracker import TrackerWindow


class TrackerEditorMenu(QWidget):
    def __init__(self, config: Config, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = config
        self.prev_item: Optional[InventoryItem] = None

        first_item = self.config.active_inv.items[0]

        # items section
        self.label_selected_items = QLabel("Items", self)
        self.label_selected_items.setGeometry(10, 10, 70, 20)
        self.list_selected = QListView(self)
        self.list_selected.setGeometry(10, 30, 240, 570)

        self.model_cache: list[tuple[bool, str, QPixmap]] = []
        for item in self.config.active_inv.items:
            self.model_cache.append((True, item.name, item.pixmap_item.pixmap().scaled(32, 32)))
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
        self.group_pos.setGeometry(260, 70, 251, 191)

        self.table_pos = QTableWidget(self.group_pos)
        self.table_pos.setGeometry(10, 30, 231, 121)
        self.table_pos.setColumnCount(3)
        self.table_pos.setHorizontalHeaderItem(0, QTableWidgetItem("X"))
        self.table_pos.setHorizontalHeaderItem(1, QTableWidgetItem("Y"))
        self.table_pos.setHorizontalHeaderItem(2, QTableWidgetItem("Angle"))
        self.table_pos.horizontalHeader().setDefaultSectionSize(60)
        self.table_pos.setRowCount(len(first_item.positions))

        for i, pos in enumerate(first_item.positions):
            self.table_pos.setVerticalHeaderItem(i, QTableWidgetItem(f"Pos. {i + 1}"))
            self.table_pos.setItem(i, 0, QTableWidgetItem(f"{pos.x}"))
            self.table_pos.setItem(i, 1, QTableWidgetItem(f"{pos.y}"))
            self.table_pos.setItem(i, 2, QTableWidgetItem("0.0"))

        self.btn_table_add = QPushButton("Add", self.group_pos)
        self.btn_table_add.setGeometry(9, 160, 111, 21)
        self.btn_table_del = QPushButton("Remove", self.group_pos)
        self.btn_table_del.setGeometry(130, 160, 111, 21)

        self.group_sources = QGroupBox("Icon Paths", self)
        self.group_sources.setGeometry(260, 270, 251, 331)

        self.list_sources = QListView(self.group_sources)
        self.list_sources.setGeometry(10, 30, 231, 271)

        self.model_cache_sources: list[tuple[bool, str, QPixmap]] = []
        for src_item in first_item.sources:
            self.model_cache_sources.append((True, src_item.name, QPixmap(str(src_item.path))))
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()
        # self.model_sources.currentChanged.connect(self.selection_changed)

        self.btn_sources_add = QPushButton("Add", self.group_sources)
        self.btn_sources_add.setGeometry(9, 305, 71, 21)
        self.btn_sources_del = QPushButton("Remove", self.group_sources)
        self.btn_sources_del.setGeometry(89, 305, 71, 21)
        self.btn_sources_open = QPushButton("Open File", self.group_sources)
        self.btn_sources_open.setGeometry(170, 305, 71, 21)

        self.group_counters = QGroupBox("Use Counters", self)
        self.group_counters.setGeometry(520, 30, 521, 301)
        self.group_counters.setCheckable(True)
        self.group_counters.setChecked(False)

        self.table_counters = QTableWidget(self.group_counters)
        self.table_counters.setGeometry(10, 30, 501, 241)
        self.table_counters.setColumnCount(1)
        self.table_counters.setHorizontalHeaderItem(0, QTableWidgetItem("Counter 1"))
        self.table_counters.setRowCount(7)
        self.table_counters.setVerticalHeaderItem(0, QTableWidgetItem("Text Settings Index"))
        self.table_counters.setVerticalHeaderItem(1, QTableWidgetItem("Minimum"))
        self.table_counters.setVerticalHeaderItem(2, QTableWidgetItem("Maximum"))
        self.table_counters.setVerticalHeaderItem(3, QTableWidgetItem("Increment"))
        self.table_counters.setVerticalHeaderItem(4, QTableWidgetItem("Position (rel.)"))
        self.table_counters.setVerticalHeaderItem(5, QTableWidgetItem("Width"))
        self.table_counters.setVerticalHeaderItem(6, QTableWidgetItem("Height"))

        self.btn_counters_add = QPushButton("Add", self.group_counters)
        self.btn_counters_add.setGeometry(9, 274, 111, 21)
        self.btn_counters_del = QPushButton("Remove", self.group_counters)
        self.btn_counters_del.setGeometry(130, 274, 111, 21)

        self.group_rewards = QGroupBox("Use Rewards", self)
        self.group_rewards.setGeometry(520, 340, 521, 261)
        self.group_rewards.setCheckable(True)
        self.group_rewards.setChecked(False)

        self.table_rewards = QTableWidget(self.group_rewards)
        self.table_rewards.setGeometry(10, 30, 501, 201)
        self.table_rewards.setColumnCount(1)
        self.table_rewards.setHorizontalHeaderItem(0, QTableWidgetItem("Reward 1"))
        self.table_rewards.setRowCount(5)
        self.table_rewards.setVerticalHeaderItem(0, QTableWidgetItem("Text Settings Index"))
        self.table_rewards.setVerticalHeaderItem(1, QTableWidgetItem("Name"))
        self.table_rewards.setVerticalHeaderItem(2, QTableWidgetItem("Position (rel.)"))
        self.table_rewards.setVerticalHeaderItem(3, QTableWidgetItem("Width"))
        self.table_rewards.setVerticalHeaderItem(4, QTableWidgetItem("Height"))

        self.btn_rewards_add = QPushButton("Add", self.group_rewards)
        self.btn_rewards_add.setGeometry(9, 233, 111, 21)
        self.btn_rewards_del = QPushButton("Remove", self.group_rewards)
        self.btn_rewards_del.setGeometry(130, 233, 111, 21)

        self.group_extras = QGroupBox("Use Extras", self)
        self.group_extras.setGeometry(520, 610, 101, 101)
        self.group_extras.setCheckable(True)
        self.group_extras.setChecked(False)

        self.label_extra_index = QLabel("Extra Index", self.group_extras)
        self.label_extra_index.setGeometry(10, 31, 81, 18)
        self.extra_index = QSpinBox(self.group_extras)
        self.extra_index.setGeometry(9, 57, 81, 32)
        self.extra_index.setMinimum(0)

        self.group_flags = QGroupBox("Use Flags", self)
        self.group_flags.setGeometry(630, 610, 101, 101)
        self.group_flags.setCheckable(True)
        self.group_flags.setChecked(False)

        self.label_flag_index = QLabel("Flag Index", self.group_flags)
        self.label_flag_index.setGeometry(10, 31, 81, 18)
        self.flag_index = QSpinBox(self.group_flags)
        self.flag_index.setGeometry(9, 57, 81, 32)
        self.flag_index.setMinimum(0)

        self.group_bg = QGroupBox("Background Settings", self)
        self.group_bg.setGeometry(740, 610, 301, 101)

        self.bg_color = QLineEdit(self.group_bg)
        self.bg_color.setGeometry(9, 27, 171, 32)
        self.bg_color.setText(f"#{Color.pack(config.active_inv.background_color):06X}")
        self.label_bg_color = QLabel("Background Color", self.group_bg)
        self.label_bg_color.setGeometry(185, 33, 121, 18)

        self.bg_path = QLineEdit(self.group_bg)
        self.bg_path.setReadOnly(True)
        self.bg_path.setGeometry(9, 65, 171, 32)
        self.bg_path.setText(f"{config.active_inv.background}")
        self.btn_bg_open_file = QPushButton("Open File", self.group_bg)
        self.btn_bg_open_file.setGeometry(183, 65, 111, 32)

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

    def clear_prev_item_flags(self):
        if self.prev_item is not None:
            self.prev_item.pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.prev_item.pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def selection_changed(self):
        item = self.get_item()

        self.item_name.setText(item.name)

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
                table_item.setText(f"{item.pixmap_item.rotation()}")
            else:
                self.table_pos.setItem(i, 2, QTableWidgetItem(f"{item.pixmap_item.rotation()}"))

        self.model_cache_sources.clear()
        for src_item in item.sources:
            self.model_cache_sources.append((True, src_item.name, QPixmap(str(src_item.path))))
        self.list_sources.model().deleteLater()
        self.list_sources.setModel(ListViewModel(self.model_cache_sources))
        self.list_sources.setCurrentIndex(self.list_sources.model().index(0, 0))
        self.model_sources = self.list_sources.selectionModel()

        self.group_extras.setChecked(item.extra_index is not None)
        if item.extra_index is not None:
            self.extra_index.setValue(item.extra_index)

        self.group_flags.setChecked(item.flag_index is not None)
        if item.flag_index is not None:
            self.flag_index.setValue(item.flag_index)

        self.clear_prev_item_flags()
        item.pixmap_item.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        item.pixmap_item.setSelected(True)

        self.prev_item = item

    def update_pos_x(self, value: int):
        item = self.get_item()
        item.pixmap_item.setPos(value, self.pos_y.value())

        if len(item.positions) == 1:
            item.positions[0].x = value

    def update_pos_y(self, value: int):
        item = self.get_item()
        item.pixmap_item.setPos(self.pos_x.value(), value)

        if len(item.positions) == 1:
            item.positions[0].y = value

    def update_pos(self, new_pos: QPoint):
        self.pos_x.setValue(new_pos.x())
        self.pos_y.setValue(new_pos.y())

    def update_angle(self, value: int):
        item = self.get_item()
        item.pixmap_item.setRotation(value)
        item.rotation = value

    def save_config(self):
        self.config.to_xml()
        print("Config saved successfully!")

    def add_item(self):
        pass

    def remove_item(self):
        item = self.get_item()
        scene = item.pixmap_item.scene()

        if scene is not None:
            self.model_cache.pop(item.index)
            self.config.active_inv.remove_item(item.index)

            if item.pixmap_item.label_counter is not None:
                scene.removeItem(item.pixmap_item.label_counter)

            scene.removeItem(item.pixmap_item)
            self.list_selected.viewport().update()

    def update_item_name(self):
        item = self.get_item()
        item.name = self.item_name.text()

        index = self.list_selected.currentIndex().row()
        model_item = self.model_cache[index]
        model_item = (model_item[0], item.name, model_item[2])
        self.model_cache[index] = model_item
        self.list_selected.update(self.list_selected.currentIndex())


class TrackerEditor(TrackerWindow):
    def __init__(self, parent: Optional[QWidget], configs: dict[Path, Config], config_index: int):
        super().__init__(parent, configs, config_index, True)

        self.edit_menu = TrackerEditorMenu(self.config)
        self.config.edit_menu = self.edit_menu
        self.config.edit_menu.list_selected.clearSelection()

    def closeEvent(self, e):
        self.edit_menu.close()
        super().closeEvent(e)

    def update_window(self):
        if self.config.edit_menu is not None:
            self.config.edit_menu.clear_prev_item_flags()
            super().update_window()

            self.config.edit_menu = self.edit_menu
            self.config.edit_menu.config = self.config
            self.config.edit_menu.prev_item = None
            self.config.edit_menu.list_selected.clearSelection()
