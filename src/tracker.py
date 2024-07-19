import sys
import os
import time

from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image
from PyQt6.QtGui import QIcon, QPixmap, QAction, QCloseEvent
from PyQt6.QtCore import QSize, Qt, QRect, QThread
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


class AutosaveThread(QThread):
    def __init__(self, parent: Optional[QWidget], config: Config):
        super().__init__()

        self.setParent(parent)
        self.config = config
        self.run_ = False

    def run(self):
        while self.run_:
            # every 5 minutes
            # TODO: configurable time
            time.sleep(5 * 60)

            if self.config.autosave_enabled:
                folder = Path("autosaves/").resolve()
                if not folder.exists():
                    folder.mkdir(parents=True, exist_ok=True)

                if self.config.state_path is None:
                    now = datetime.now()
                    filename = f"autosave_{now.strftime('%d-%m-%Y')}_{now.strftime('%H-%M-%S')}.txt"
                    path = folder / filename
                else:
                    path = self.config.state_path

                state = State(self.config, path)
                state.save()


class TrackerWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget], config: Config):
        super().__init__()

        self.parent_ = parent
        self.config = config
        self.bg_path = self.config.active_inv.background

        self.task = AutosaveThread(self, config)
        self.task.start()

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

        if not self.config.state_saved:
            answer = QMessageBox.question(
                self,
                "Warning",
                "Quit without saving the tracker's progress?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if answer == QMessageBox.StandardButton.No:
                e.ignore()
                return

        # stop the loop and wait until the execution is finished
        # TODO: something better than this
        self.task.run_ = False
        while self.task.isRunning():
            pass

        for item in self.config.active_inv.items:
            item.reward_map = {}

        if self.parent_ is not None:
            self.parent_.show()
            self.close()

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
        color = self.config.active_inv.background_color
        self.bg = QFrame(self.centralwidget)
        self.bg.setObjectName("bg")
        self.bg.setGeometry(QRect(0, 0, width, height))
        self.bg.setMinimumSize(QSize(width, height))
        self.bg.setMaximumSize(QSize(width, height))
        self.bg.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet(f"background-color: rgb({color.r}, {color.g}, {color.b});")
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

        self.action_close = QAction(self.menu_file)
        self.action_close.setObjectName("action_close")
        self.action_close.setText("Close")
        self.action_close.triggered.connect(self.file_close_triggered)

        self.action_exit = QAction(self.menu_file)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setText("Exit")
        self.action_exit.triggered.connect(self.file_exit_triggered)

        self.action_autosave = QAction(self.menu_file)
        self.action_autosave.setCheckable(True)
        self.action_autosave.setObjectName("action_autosave")
        self.action_autosave.setText("Autosave (5 min)")
        self.action_autosave.triggered.connect(self.file_autosave_triggered)

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_autosave)
        self.menu_file.addAction(self.action_close)
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
                        item.counter.text_settings_index,
                    )

                    # emit a click if the counter label is clicked (workaround for priority)
                    label.label_counter.item_label = label
                    label.label_counter.clicked_left.connect(self.outlinedLabel_clicked_left)
                    label.label_counter.clicked_middle.connect(self.outlinedLabel_clicked_middle)
                    label.label_counter.clicked_right.connect(self.outlinedLabel_clicked_right)

                if item.is_reward:
                    reward_info = self.config.active_inv.rewards.items[label.reward_index]
                    geometry = QRect(
                        pos.x + reward_info.pos.x, pos.y + reward_info.pos.y, reward_info.width, reward_info.height
                    )

                    if item.reward_map.get(i) is not None:
                        item.reward_map[i].setGeometry(geometry)
                        item.reward_map[i].setText(reward_info.name)
                    else:
                        item.reward_map[i] = OutlinedLabel.new(
                            self.centralwidget,
                            self.config,
                            f"{obj_name}_reward",
                            geometry,
                            reward_info.name,
                            reward_info.text_settings_index,
                        )

                    if item.reward_map[i].item_label is None:
                        item.reward_map[i].item_label = label
                    label.raise_()

                if item.extra_index is not None:
                    extra = self.config.extras.items[item.extra_index]
                    width, height = Image.open(extra.path).size
                    label.label_extra_img = Label.new(
                        self.config,
                        self.centralwidget,
                        item.index,
                        item.name,
                        f"{obj_name}_extra_img",
                        QRect(pos.x + extra.pos.x, pos.y + extra.pos.y, width, height),
                        str(extra.path),
                        1.0,
                        False,
                        0.0,
                    )

                    label.label_extra_img.setVisible(False)
                    label.label_extra_img.clicked_left.connect(self.label_clicked_left)
                    label.label_extra_img.clicked_middle.connect(self.label_clicked_middle)
                    label.label_extra_img.clicked_right.connect(self.label_clicked_right)

                if len(self.config.flags) > 0 and item.flag_index is not None:
                    flag = self.config.flags[item.flag_index]
                    label.label_flag = OutlinedLabel.new(
                        self.centralwidget,
                        self.config,
                        f"{obj_name}_flag",
                        QRect(pos.x + flag.pos.x, pos.y + flag.pos.y, flag.width, flag.height),
                        flag.texts[label.flag_text_index],
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

    def file_autosave_triggered(self):
        self.config.autosave_enabled = self.action_autosave.isChecked()
        self.task.run_ = self.config.autosave_enabled

    def file_close_triggered(self):
        self.close()

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
        self.config.state_saved = False

    def label_clicked_middle(self):
        label: Label = self.sender()
        self.config.state_saved = False

        if label.label_flag is not None:
            label.label_flag.setVisible(not label.label_flag.isVisible())
        else:
            label.update_label(True, True)

    def label_clicked_right(self):
        label: Label = self.sender()
        self.config.state_saved = False
        item = self.config.active_inv.items[label.index]

        if item.is_reward:
            for i, _ in enumerate(item.positions):
                if label.objectName().endswith(f"_pos_{i}"):
                    reward = item.reward_map[i]

                    if reward is not None and reward.item_label is not None:
                        label.reward_index += 1

                        if label.reward_index > len(self.config.active_inv.rewards.items) - 1:
                            label.reward_index = 0

                        item.update_reward(i, self.config.active_inv.rewards.items[label.reward_index])
        elif label.label_extra_img is not None:
            label.label_extra_img.setVisible(not label.label_extra_img.isVisible())
        else:
            label.update_label(False)

    def label_gomode_clicked_left(self):
        label: Label = self.sender()
        label.update_gomode()

    def label_gomode_clicked_right(self):
        label: Label = self.sender()
        label.update_gomode()
