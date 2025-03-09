from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QListView, QPushButton, QSpinBox, QGraphicsItem

from common import ListViewModel
from config import Config, InventoryItem
from tracker import TrackerWindow


class TrackerEditorMenu(QWidget):
    def __init__(self, config: Config, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = config

        self.label_selected_items = QLabel("Item List", self)
        self.label_selected_items.setGeometry(10, 10, 90, 18)

        self.list_selected = QListView(self)
        self.list_selected.setGeometry(10, 30, 240, 390)

        self.model_cache: list[tuple[bool, str, QPixmap]] = []

        for item in self.config.active_inv.items:
            self.model_cache.append((True, item.name, item.pixmap_item.pixmap().scaled(32, 32)))

        self.list_selected.setModel(ListViewModel(self.model_cache))
        model = self.list_selected.selectionModel()
        model.currentChanged.connect(self.selection_changed)

        self.label_pos_x = QLabel("X", self)
        self.label_pos_x.setGeometry(280, 30, 16, 20)

        self.pos_x = QSpinBox(self)
        self.pos_x.setGeometry(260, 50, 50, 30)
        self.pos_x.setMaximum(999)
        self.pos_x.valueChanged.connect(self.update_pos_x)

        self.label_pos_y = QLabel("Y", self)
        self.label_pos_y.setGeometry(330, 30, 16, 20)

        self.pos_y = QSpinBox(self)
        self.pos_y.setGeometry(310, 50, 50, 30)
        self.pos_y.setMaximum(999)
        self.pos_y.valueChanged.connect(self.update_pos_y)

        self.label_angle = QLabel("Angle", self)
        self.label_angle.setGeometry(368, 30, 41, 20)

        self.angle = QSpinBox(self)
        self.angle.setGeometry(360, 50, 50, 30)
        self.angle.setMaximum(360)
        self.angle.valueChanged.connect(self.update_angle)

        self.btn_save = QPushButton("Save Config", self)
        self.btn_save.setGeometry(370, 388, 90, 35)
        self.btn_save.pressed.connect(self.save_config)

        self.setGeometry(0, 0, 470, 430)
        self.setFixedSize(470, 430)
        self.setWindowTitle("Tracker Editor")

        # start centered
        qtRectangle = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.show()

        self.prev_item: Optional[InventoryItem] = None

    def get_item(self):
        return self.config.active_inv.items[self.list_selected.currentIndex().row()]

    def clear_prev_item_flags(self):
        if self.prev_item is not None:
            self.prev_item.pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.prev_item.pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def selection_changed(self):
        item = self.get_item()
        pos = item.pixmap_item.pos()
        self.pos_x.setValue(int(pos.x()))
        self.pos_y.setValue(int(pos.y()))
        self.angle.setValue(int(item.pixmap_item.rotation()))
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
