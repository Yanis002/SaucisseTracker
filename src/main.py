#!/usr/bin/env python3

import sys
import os

from pathlib import Path

from PIL import Image
from PyQt6.QtGui import QIcon, QPixmap, QAction, QColor
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMainWindow,
    QFrame,
    QMenu,
    QMenuBar,
    QApplication,
    QFileDialog,
    QGraphicsColorizeEffect,
)

from common import OutlinedLabel, Label, get_new_path, GLOBAL_HALF_OPACITY
from config import Config
from state import State


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Made with ♥ by Yanis.\n\nLicensed under GNU General Public License v3.0"))
        self.setLayout(layout)
        self.create_window(320, 100)

    def create_window(self, width: int, height: int):
        # initialize the window's basic informations
        self.setWindowTitle("SaucisseTracker - About")
        self.setWindowIcon(QIcon(get_new_path("res/icon.png", True)))
        self.resize(width, height)
        self.setMinimumSize(QSize(width, height))
        self.setMaximumSize(QSize(width, height))
        self.setAutoFillBackground(False)


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        super().__init__()

        self.config = config
        self.bg_path = get_new_path(f"config/oot/{self.config.active_inv.background}")

        # get the background's size
        width, height = Image.open(self.bg_path).size

        # create the window itself
        self.create_window(width, height)

        # create the background image
        self.create_background(width, height)

        # create the top menu bar
        self.create_menubar()

        # create the necessary labels based on the config
        self.create_labels()

        # create the about window
        self.about_window = AboutWindow()
        self.about_window.setObjectName("about_window")

    def create_window(self, width: int, height: int):
        # accounts for platform differences for the windows' size
        offset = 34 if os.name == "nt" else 20

        # initialize the window's basic informations
        self.setWindowTitle("SaucisseTracker")
        self.setWindowIcon(QIcon(get_new_path("res/icon.png", True)))
        self.resize(width, height + offset)
        self.setMinimumSize(QSize(width, height + offset))
        self.setMaximumSize(QSize(width, height + offset))
        self.setAutoFillBackground(False)

        # create the central widget
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

    def create_background(self, width: int, height: int):
        self.bg = QFrame(self.centralwidget)
        self.bg.setObjectName("bg")
        self.bg.setGeometry(QRect(0, 0, width, height))
        self.bg.setMinimumSize(QSize(width, height))
        self.bg.setMaximumSize(QSize(width, height))
        self.bg.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.bg.setFrameShape(QFrame.Shape.StyledPanel)
        self.bg.setFrameShadow(QFrame.Shadow.Raised)
        self.bg.setLineWidth(1)

        # for some reasons using stylesheet for bg doesn't work on windows but this does :)
        bg_label = QLabel(self.bg)
        bg_label.setObjectName(f"bg_label")
        bg_label.setGeometry(QRect(0, 0, width, height))
        bg_label.setText("")
        bg_label.setPixmap(QPixmap(get_new_path(self.bg_path)))

    def create_menubar(self):
        self.menu = QMenuBar(parent=self)
        self.menu.setObjectName("menu")
        self.menu.setGeometry(QRect(0, 0, 335, 21))

        self.menu_file = QMenu(parent=self.menu)
        self.menu_file.setObjectName("menu_file")
        self.menu_file.setTitle("File")

        self.action_about = QAction(parent=self.menu)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.triggered.connect(self.about_triggered)

        self.action_open = QAction(self.menu_file)
        self.action_open.setObjectName("action_open")
        self.action_open.setText("Open State")
        self.action_open.triggered.connect(self.file_open_triggered)

        self.action_save = QAction(self.menu_file)
        self.action_save.setObjectName("action_save")
        self.action_save.setText("Save State")
        self.action_save.triggered.connect(self.file_save_triggered)

        self.action_exit = QAction(self.menu_file)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setText("Exit")
        self.action_exit.triggered.connect(self.file_exit_triggered)

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_exit)
        self.menu.addAction(self.menu_file.menuAction())
        self.menu.addAction(self.action_about)
        self.setMenuBar(self.menu)

    def create_labels(self):
        offset = -1 if os.name == "nt" else 0
        for item in self.config.active_inv.items:
            label_effect_map: dict[int, QGraphicsColorizeEffect] = {}
            label_map: dict[int, Label] = {}

            for i, pos in enumerate(item.positions):
                obj_name = f"item{item.index}_pos_{i}"
                img_path = get_new_path(f"config/oot/{item.paths[0]}")

                if item.scale_content:
                    width = 32
                    height = 32
                else:
                    width, height = Image.open(img_path).size

                label = Label(self.centralwidget, item.index, item.name)
                label.setObjectName(obj_name)
                label.setGeometry(QRect(pos.x + offset, pos.y + offset, width, height))
                label.setText("")
                label.original_pixmap = QPixmap(img_path)
                label.setPixmap(label.original_pixmap)
                label.set_pixmap_opacity(1.0 if item.enabled else GLOBAL_HALF_OPACITY)
                label.setScaledContents(item.scale_content)

                label.clicked_left.connect(self.label_clicked_left)
                label.clicked_middle.connect(self.label_clicked_middle)
                label.clicked_right.connect(self.label_clicked_right)

                if item.counter is not None:
                    label.label_counter = OutlinedLabel.new(
                        self.centralwidget,
                        self.config,
                        f"{obj_name}_counter",
                        QRect(pos.x + offset - 6, pos.y + 22, 32, 15),
                        "",
                        1,
                        item.counter.text_settings_index
                    )

                    # emit a click if the counter label is clicked (workaround for priority)
                    label.label_counter.item_label = label
                    label.label_counter.clicked_left.connect(self.outlinedLabel_clicked_left)
                    label.label_counter.clicked_middle.connect(self.outlinedLabel_clicked_middle)
                    label.label_counter.clicked_right.connect(self.outlinedLabel_clicked_right)

                if item.is_reward:
                    reward = self.config.active_inv.rewards.items[0]
                    label.label_reward = OutlinedLabel.new(
                        self.centralwidget,
                        self.config,
                        f"{obj_name}_reward",
                        QRect(pos.x + offset - 6, pos.y + offset + 23, 45, 32),
                        reward.name,
                        1.8,
                        reward.text_settings_index
                    )
                    label.raise_()

                # black & white effect, todo find something better? idk, enabled by default
                label_effect = QGraphicsColorizeEffect(label)
                label_effect.setStrength(0.0 if item.enabled else 1.0)
                label_effect.setColor(QColor("black"))
                label_effect.setObjectName(f"{obj_name}_fx")
                label.setGraphicsEffect(label_effect)

                label_effect_map[i] = label_effect
                label_map[i] = label

            self.config.active_inv.label_effect_map[item.index] = label_effect_map
            self.config.active_inv.label_map[item.index] = label_map

    # connections callbacks

    def file_open_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = QFileDialog.getOpenFileName(None, "Open State File", str(Path.home()), "*.txt")[0]

        if len(self.config.state_path) > 0:
            state = State(self.config)
            state.open()

    def file_save_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = QFileDialog.getSaveFileName(None, "Save State File", str(Path.home()), "*.txt")[0]

        if len(self.config.state_path) > 0:
            state = State(self.config)
            state.save()

    def file_exit_triggered(self):
        sys.exit()

    def about_triggered(self):
        if self.about_window.isVisible():
            self.about_window.hide()
        else:
            self.about_window.show()

    def outlinedLabel_clicked_left(self):
        label: OutlinedLabel = self.sender()

        if label.item_label is not None:
            label.item_label.clicked_left.emit()

    def outlinedLabel_clicked_middle(self):
        label: OutlinedLabel = self.sender()

        if label.item_label is not None:
            label.item_label.clicked_middle.emit()

    def outlinedLabel_clicked_right(self):
        label: OutlinedLabel = self.sender()

        if label.item_label is not None:
            label.item_label.clicked_right.emit()

    def label_clicked_left(self):
        label: Label = self.sender()
        label.update_label(self.config, self.config.active_inv.items[label.index], True)

    def label_clicked_middle(self):
        label: Label = self.sender()

    def label_clicked_right(self):
        label: Label = self.sender()

        if label.label_reward is not None:
            label.label_reward.reward_index += 1

            if label.label_reward.reward_index > len(self.config.active_inv.rewards.items) - 1:
                label.label_reward.reward_index = 0

            reward = self.config.active_inv.rewards.items[label.label_reward.reward_index]
            label.label_reward.setText(reward.name)
        else:
            label.update_label(self.config, self.config.active_inv.items[label.index], False)


def main():
    # taskbar icon trick for Windows
    if os.name == "nt":
        from ctypes import windll

        # encoding probably useless but just in case
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

    app = QApplication(sys.argv)
    mainWindow = MainWindow(Config(get_new_path("config/oot/config.xml")))

    mainWindow.show()
    sys.exit(app.exec())


# start the app
if __name__ == "__main__":
    main()
