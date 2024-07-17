#!/usr/bin/env python3

import sys
import os
import traceback

from pathlib import Path
from typing import Optional
from copy import copy

from PyQt6.QtGui import QIcon, QPixmap, QShowEvent
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QMainWindow,
    QApplication,
    QFileDialog,
    QPushButton,
    QLineEdit,
    QListView,
)

from common import ListViewModel, show_error
from config import Config
from tracker import TrackerWindow


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

    def showEvent(self, e: Optional[QShowEvent]):
        super(QMainWindow, self).showEvent(e)

        if self.tracker_window is not None:
            self.tracker_window = None

    # connections callbacks

    def btn_set_config_dir_clicked(self):
        try:
            path = QFileDialog.getExistingDirectory(None, "Open Splits Images Folder", str(Path.cwd()))
            if len(path) > 0:
                self.line_edit_config_folder.setText(path)
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

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
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def btn_go_clicked(self):
        try:
            if len(self.configs) > 0:
                config = list(self.configs.values())[self.list_configs.currentIndex().row()]
                self.tracker_window = TrackerWindow(self, copy(config))
                self.tracker_window.show()
                self.hide()
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")


def main():
    app = QApplication(sys.argv)

    # taskbar icon trick for Windows
    if os.name == "nt":
        from ctypes import windll

        # encoding probably useless but just in case
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


# start the app
if __name__ == "__main__":
    main()
