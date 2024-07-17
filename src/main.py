#!/usr/bin/env python3

import sys
import os

from pathlib import Path
from typing import Optional

from PIL import Image
from PyQt6.QtGui import QIcon, QPixmap, QAction, QCloseEvent
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
    QPushButton,
    QLineEdit,
    QListView,
)

from common import ListViewModel, OutlinedLabel, Label, show_error, GLOBAL_HALF_OPACITY
from config import Config, Pos
from state import State


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("Made with ♥ by Yanis.\n" + "Version 0.1.0.\n\n" + "Licensed under GNU General Public License v3.0.")
        )
        self.setLayout(layout)
        self.create_window(320, 100)

    def create_window(self, width: int, height: int):
        # initialize the window's basic informations
        self.setWindowTitle("SaucisseTracker - About")
        self.setWindowIcon(QIcon(str(Path("res/icon.png").resolve())))
        self.resize(width, height)
        self.setMinimumSize(QSize(width, height))
        self.setMaximumSize(QSize(width, height))
        self.setAutoFillBackground(False)


class TrackerWindow(QMainWindow):
    def __init__(self, main: "MainWindow", config: Config):
        super().__init__()

        self.main_window = main
        self.config = config
        self.bg_path = self.config.active_inv.background

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

    def closeEvent(self, e: Optional[QCloseEvent]):
        super(QMainWindow, self).closeEvent(e)
        self.main_window.show()

    def create_window(self, width: int, height: int):
        # accounts for platform differences for the windows' size
        offset = 34 if os.name == "nt" else 20

        # initialize the window's basic informations
        self.setWindowTitle("SaucisseTracker")
        self.setWindowIcon(QIcon(str(Path("res/icon.png").resolve())))
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
        bg_label.setPixmap(QPixmap(str(self.bg_path)))

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

        # create go mode label and light stuff
        if self.config.gomode_settings is not None:
            gomode_settings = self.config.gomode_settings
            width, height = Image.open(gomode_settings.path).size

            self.config.label_gomode = Label.new(
                self.config,
                self.centralwidget,
                0,
                "Go Mode",
                "label_gomode",
                QRect(gomode_settings.pos.x, gomode_settings.pos.y, width, height),
                str(gomode_settings.path),
                0.0 if gomode_settings.hide_if_disabled else GLOBAL_HALF_OPACITY,
                False,
                1.0,
            )

            if gomode_settings.light_path is not None and gomode_settings.light_pos is not None:
                width, height = Image.open(gomode_settings.light_path).size

                self.config.label_gomode_light = Label.new(
                    self.config,
                    self.centralwidget,
                    0,
                    "Go Mode Light",
                    "label_gomode_light",
                    QRect(gomode_settings.light_pos.x, gomode_settings.light_pos.y, width, height),
                    str(gomode_settings.light_path),
                    1.0,
                    False,
                    0.0,
                )

                self.config.label_gomode_light.setVisible(False)
                self.config.label_gomode.raise_()

            self.config.label_gomode.clicked_left.connect(self.label_gomode_clicked_left)
            self.config.label_gomode.clicked_right.connect(self.label_gomode_clicked_right)

        # create labels for every items of the active inventory
        for item in self.config.active_inv.items:
            label_map: dict[int, Label] = {}

            for i, item_pos in enumerate(item.positions):
                obj_name = f"item{item.index}_pos_{i}"
                pos = Pos(item_pos.x + offset, item_pos.y + offset)

                if item.scale_content:
                    width = 32
                    height = 32
                else:
                    width, height = Image.open(item.paths[0]).size

                label = Label.new(
                    self.config,
                    self.centralwidget,
                    item.index,
                    item.name,
                    obj_name,
                    QRect(pos.x, pos.y, width, height),
                    str(item.paths[0]),
                    1.0 if item.enabled else GLOBAL_HALF_OPACITY,
                    item.scale_content,
                    0.0 if item.enabled else 1.0,
                )

                label.clicked_left.connect(self.label_clicked_left)
                label.clicked_middle.connect(self.label_clicked_middle)
                label.clicked_right.connect(self.label_clicked_right)

                if item.counter is not None:
                    label.label_counter = OutlinedLabel.new(
                        self.centralwidget,
                        self.config,
                        f"{obj_name}_counter",
                        QRect(
                            pos.x + item.counter.pos.x,
                            pos.y + item.counter.pos.y,
                            item.counter.width,
                            item.counter.height,
                        ),
                        "",
                        1,
                        item.counter.text_settings_index,
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
                        QRect(pos.x - 6, pos.y + 23, 45, 32),
                        reward.name,
                        1.8,
                        reward.text_settings_index,
                    )
                    label.raise_()

                if item.use_checkmark:
                    label.label_check = Label.new(
                        self.config,
                        self.centralwidget,
                        item.index,
                        item.name,
                        f"{obj_name}_checkmark",
                        QRect(pos.x + 18, pos.y - 4, 16, 16),
                        str(self.config.active_inv.song_check_path),
                        1.0,
                        False,
                        0.0,
                    )

                    label.label_check.setVisible(False)
                    label.label_check.clicked_left.connect(self.label_clicked_left)
                    label.label_check.clicked_middle.connect(self.label_clicked_middle)
                    label.label_check.clicked_right.connect(self.label_clicked_right)

                if len(self.config.flags) > 0 and item.flag_index is not None:
                    flag = self.config.flags[item.flag_index]
                    label.label_flag = OutlinedLabel.new(
                        self.centralwidget,
                        self.config,
                        f"{obj_name}_flag",
                        QRect(pos.x + flag.pos.x, pos.y + flag.pos.y, 35, 15),
                        flag.texts[label.flag_text_index],
                        1.8,
                        flag.text_settings_index,
                    )
                    label.label_flag.setHidden(flag.hidden)

                    label.label_flag.item_label = label
                    label.label_flag.clicked_left.connect(self.outlinedLabel_clicked_left)
                    label.label_flag.clicked_middle.connect(self.outlinedLabel_clicked_middle)
                    label.label_flag.clicked_right.connect(self.outlinedLabel_clicked_right)

                label_map[i] = label

            self.config.active_inv.label_map[item.index] = label_map

    # connections callbacks

    def file_open_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = Path(
                QFileDialog.getOpenFileName(None, "Open State File", str(Path.home()), "*.txt")[0]
            ).resolve()

        if self.config.state_path.exists():
            state = State(self.config)
            state.open()

    def file_save_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = Path(
                QFileDialog.getSaveFileName(None, "Save State File", str(Path.home()), "*.txt")[0]
            ).resolve()

        if self.config.state_path.exists():
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
        label.update_label(True)

    def label_clicked_middle(self):
        label: Label = self.sender()

        if label.label_flag is not None:
            label.label_flag.setVisible(not label.label_flag.isVisible())
        else:
            label.update_label(True, True)

    def label_clicked_right(self):
        label: Label = self.sender()

        if label.label_reward is not None:
            label.label_reward.reward_index += 1

            if label.label_reward.reward_index > len(self.config.active_inv.rewards.items) - 1:
                label.label_reward.reward_index = 0

            reward = self.config.active_inv.rewards.items[label.label_reward.reward_index]
            label.label_reward.setText(reward.name)
        elif label.label_check is not None:
            label.label_check.setVisible(not label.label_check.isVisible())
        else:
            label.update_label(False)

    def label_gomode_clicked_left(self):
        label: Label = self.sender()
        label.update_gomode()

    def label_gomode_clicked_right(self):
        label: Label = self.sender()
        label.update_gomode()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.configs: dict[Path, Config] = {}
        self.config_dir = Path()
        self.model_cache: list[tuple[bool, str, QPixmap]] = []
        self.tracker_window: Optional[TrackerWindow] = None

        self.setWindowTitle("SaucisseTracker")
        self.setObjectName("MainWindow")
        self.resize(275, 371)
        self.setMinimumSize(QSize(275, 371))
        self.setMaximumSize(QSize(275, 371))
        self.setWindowIcon(QIcon(str(Path("res/icon.png").resolve())))

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.btn_set_config_dir = QPushButton(self.centralwidget)
        self.btn_set_config_dir.setObjectName("btn_set_config_dir")
        self.btn_set_config_dir.setGeometry(QRect(224, 29, 41, 23))
        self.btn_set_config_dir.setText("Set")

        self.line_edit_config_folder = QLineEdit(self.centralwidget)
        self.line_edit_config_folder.setObjectName("line_edit_config_folder")
        self.line_edit_config_folder.setGeometry(QRect(10, 30, 211, 20))
        self.line_edit_config_folder.setReadOnly(True)

        self.label_found = QLabel(self.centralwidget)
        self.label_found.setObjectName("label_found")
        self.label_found.setGeometry(QRect(10, 60, 130, 16))
        self.label_found.setText("Found configurations")

        self.label_config_folder = QLabel(self.centralwidget)
        self.label_config_folder.setObjectName("label_config_folder")
        self.label_config_folder.setGeometry(QRect(10, 10, 120, 16))
        self.label_config_folder.setText("Configuration folder")

        self.btn_go = QPushButton(self.centralwidget)
        self.btn_go.setObjectName("btn_go")
        self.btn_go.setGeometry(QRect(10, 310, 256, 51))
        self.btn_go.setStyleSheet('font: 75 15pt "MS Shell Dlg 2";')
        self.btn_go.setText("GO!")

        self.btn_new = QPushButton(self.centralwidget)
        self.btn_new.setObjectName("btn_new")
        self.btn_new.setGeometry(QRect(10, 280, 75, 23))
        self.btn_new.setText("New")

        self.btn_edit = QPushButton(self.centralwidget)
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setGeometry(QRect(100, 280, 75, 23))
        self.btn_edit.setText("Edit")

        self.btn_delete = QPushButton(self.centralwidget)
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setGeometry(QRect(190, 280, 75, 23))
        self.btn_delete.setText("Delete")

        self.list_configs = QListView(self.centralwidget)
        self.list_configs.setObjectName("list_configs")
        self.list_configs.setGeometry(QRect(11, 80, 253, 192))

        # connections
        self.btn_set_config_dir.clicked.connect(self.btn_set_config_dir_clicked)
        self.line_edit_config_folder.textChanged.connect(self.line_edit_config_folder_update)
        self.btn_go.clicked.connect(self.btn_go_clicked)

        # set the default config folder path
        self.line_edit_config_folder.setText(str(Path("config/").resolve()))

        # not implemented yet
        self.btn_new.setEnabled(False)
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

    # connections callbacks

    def btn_set_config_dir_clicked(self):
        try:
            path = QFileDialog.getExistingDirectory(None, "Open Splits Images Folder", str(Path.cwd()))
            if len(path) > 0:
                self.line_edit_config_folder.setText(path)
        except Exception as e:
            show_error(self, f"An error occurred: {e}")

    def line_edit_config_folder_update(self):
        try:
            self.config_dir = Path(self.line_edit_config_folder.text()).resolve()
            self.configs.clear()
            self.model_cache.clear()

            # any file that is called "config." with a format extension (xml, yml, json, etc...)
            for path in sorted(self.config_dir.rglob(f"config.*")):
                absolute = path.resolve()
                self.configs[absolute] = Config(self, absolute)

            model_items = []
            for config in self.configs.values():
                model_items.append((True, config.active_inv.name, config.active_inv.icon.scaledToHeight(32)))
            self.model_cache = [(elem[0], elem[1], elem[2]) for elem in model_items]
            self.list_configs.setModel(ListViewModel(self.model_cache))
        except Exception as e:
            show_error(self, f"An error occurred: {e}")

    def btn_go_clicked(self):
        try:
            if len(self.configs) > 0:
                config = list(self.configs.values())[self.list_configs.currentIndex().row()]
                self.tracker_window = TrackerWindow(self, config)
                self.tracker_window.show()
                self.hide()
        except Exception as e:
            show_error(self, f"An error occurred: {e}")


def main():
    app = QApplication(sys.argv)

    # taskbar icon trick for Windows
    if os.name == "nt":
        from ctypes import windll

        # encoding probably useless but just in case
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

    # tracker_window = TrackerWindow(configs[0])
    # tracker_window.show()

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


# start the app
if __name__ == "__main__":
    main()
