import sys
import os

from pathlib import Path
from typing import Optional

from PIL import Image
from PyQt6.QtGui import QIcon, QPixmap, QAction, QCloseEvent
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QLabel,
    QMainWindow,
    QFrame,
    QMenu,
    QMenuBar,
    QFileDialog,
)

from common import OutlinedLabel, Label, show_message, GLOBAL_HALF_OPACITY
from config import Config, Pos
from state import State


class TrackerWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget], config: Config):
        super().__init__()

        self.parent_ = parent
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

    def closeEvent(self, e: Optional[QCloseEvent]):
        super(QMainWindow, self).closeEvent(e)

        if self.parent_ is not None:
            self.parent_.show()

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
        show_message(
            self,
            "About",
            QMessageBox.Icon.Information,
            "Made with ♥ by Yanis.\n" + "Version 0.1.0.\n\n" + "Licensed under GNU General Public License v3.0.",
        )

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
