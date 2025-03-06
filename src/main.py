#!/usr/bin/env python3

import argparse
import os
import sys
import traceback

from copy import copy
from pathlib import Path
from shutil import copytree, rmtree
from typing import Optional
from zipfile import ZipFile

from PyQt6.QtGui import QAction, QCloseEvent, QGuiApplication, QIcon, QPixmap, QShowEvent
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QWidget,
)

from common import ListViewModel, show_error, show_info, OS_MENU_OFFSET, CURRENT_XML_VERSION
from config import Config
from tracker import TrackerWindow

TEMP_DIR = Path("temp").resolve()
TEMP_ICONS_DIR = TEMP_DIR / "icons"
TEMP_CONFIG_DIR = TEMP_DIR / "config"


class MainWindow(QMainWindow):
    """
    This class represents the window of the main menu,
    it handles reading and initializing configurations and going in the sub-modes (editor and tracker).
    """

    def __init__(self, is_debug: bool):
        """Creates the widgets of the main menu and binds them to function callbacks when required."""

        super().__init__()

        self.configs: dict[str, Config] = {}
        self.config_dir = Path()
        self.model_cache: list[tuple[bool, str, QPixmap]] = []
        self.tracker_window: Optional[TrackerWindow] = None
        self.is_debug = is_debug

        self.setWindowTitle("SaucisseTracker")
        self.setObjectName("MainWindow")
        self.setFixedSize(QSize(275, 355))
        icon_path = Path(str(Path(__file__).resolve().parent).removesuffix("src")).resolve() / "res/icon.png"
        self.setWindowIcon(QIcon(str(icon_path)))

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.btn_set_config_dir = QPushButton(self.centralwidget)
        self.btn_set_config_dir.setObjectName("btn_set_config_dir")
        self.btn_set_config_dir.setGeometry(QRect(224, 44, 41, 23))
        self.btn_set_config_dir.setText("Set")

        self.line_edit_config_folder = QLineEdit(self.centralwidget)
        self.line_edit_config_folder.setObjectName("line_edit_config_folder")
        self.line_edit_config_folder.setGeometry(QRect(10, 45, 211, 20))
        self.line_edit_config_folder.setReadOnly(True)

        self.label_found = QLabel(self.centralwidget)
        self.label_found.setObjectName("label_found")
        self.label_found.setGeometry(QRect(10, 75, 130, 16))
        self.label_found.setText("Found configurations")

        self.label_config_folder = QLabel(self.centralwidget)
        self.label_config_folder.setObjectName("label_config_folder")
        self.label_config_folder.setGeometry(QRect(10, 25, 120, 16))
        self.label_config_folder.setText("Configuration folder")

        self.btn_go = QPushButton(self.centralwidget)
        self.btn_go.setObjectName("btn_go")
        self.btn_go.setGeometry(QRect(10, 295, 256, 51))
        self.btn_go.setStyleSheet('font: 75 15pt "MS Shell Dlg 2";')
        self.btn_go.setText("GO!")

        self.list_configs = QListView(self.centralwidget)
        self.list_configs.setObjectName("list_configs")
        self.list_configs.setGeometry(QRect(11, 95, 253, 192))

        # menu
        self.menu = QMenuBar(parent=self)
        self.menu.setObjectName("menu")
        self.menu.setGeometry(QRect(0, 0, 275, OS_MENU_OFFSET))

        self.menu_file = QMenu(parent=self.menu)
        self.menu_file.setObjectName("main_menu_file")
        self.menu_file.setTitle("File")

        self.action_new = QAction(parent=self.menu_file)
        self.action_new.setObjectName("action_new")
        self.action_new.setText("New")

        self.action_edit = QAction(parent=self.menu_file)
        self.action_edit.setObjectName("action_edit")
        self.action_edit.setText("Edit")

        self.action_duplicate = QAction(parent=self.menu_file)
        self.action_duplicate.setObjectName("action_duplicate")
        self.action_duplicate.setText("Duplicate")

        self.action_delete = QAction(parent=self.menu_file)
        self.action_delete.setObjectName("action_delete")
        self.action_delete.setText("Delete")

        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_edit)
        self.menu_file.addAction(self.action_duplicate)
        self.menu_file.addAction(self.action_delete)

        self.menu.addAction(self.menu_file.menuAction())

        # connections
        self.btn_set_config_dir.clicked.connect(self.btn_set_config_dir_clicked)
        self.line_edit_config_folder.textChanged.connect(self.update_config_list)
        self.btn_go.clicked.connect(self.btn_go_clicked)
        self.list_configs.doubleClicked.connect(self.btn_go_clicked)
        self.action_new.triggered.connect(self.action_new_triggered)
        self.action_edit.triggered.connect(self.action_edit_triggered)
        self.action_duplicate.triggered.connect(self.action_duplicate_triggered)
        self.action_delete.triggered.connect(self.action_delete_triggered)

        # set the default config folder path
        self.line_edit_config_folder.setText(str(Path("config/").resolve()))

        # start centered
        qtRectangle = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        if is_debug:
            self.btn_go_clicked()

    def showEvent(self, e: Optional[QShowEvent]):
        """Actions to do when the window is showing."""

        super(QMainWindow, self).showEvent(e)

        # if the folder isn't empty
        if any(TEMP_CONFIG_DIR.iterdir()):
            rmtree(TEMP_CONFIG_DIR)
            TEMP_CONFIG_DIR.mkdir()
            self.configs.pop(str(TEMP_CONFIG_DIR / "config.xml"))

        if self.tracker_window is not None:
            self.tracker_window.deleteLater()

    def closeEvent(self, e: Optional[QCloseEvent]):
        """Actions to do when the window is closing (not hiding)."""

        super(QMainWindow, self).closeEvent(e)

        # delete the temporary folder
        rmtree(TEMP_DIR)

    # connections callbacks

    def btn_set_config_dir_clicked(self):
        """Asks the user which directory to use and set the line edit's value with the path (if chosen)."""

        try:
            path = QFileDialog.getExistingDirectory(None, "Open Splits Images Folder", str(Path.cwd()))
            if len(path) > 0:
                self.line_edit_config_folder.setText(path)
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def get_configs(self, dir: Path):
        """Finds config files (any format) and creates a new `Config`, note that each format requires its own parser."""

        # any file that is called "config." with a format extension (xml, yml, json, etc...)
        for path in sorted(dir.rglob("config.*")):
            absolute = path.resolve()
            new_config = Config(self, absolute)

            if not self.is_debug and new_config.xml_version < CURRENT_XML_VERSION:
                # previously the config's name was defined based on the first inventory name
                show_info(self, f"Ignoring outdated config named '{new_config.active_inv.name}'.")
            else:
                self.configs[str(absolute)] = new_config

    def get_config(self):
        """Returns the `Config` for the selected element in the list."""

        return list(self.configs.values())[self.list_configs.currentIndex().row()]

    def update_config_list(self):
        """Populates the config list."""

        try:
            self.config_dir = Path(self.line_edit_config_folder.text()).resolve()
            self.configs.clear()
            self.model_cache.clear()
            model_items = []

            if not self.config_dir.exists():
                show_info(self, f"This path does not exist ('{self.config_dir}').")
                return

            # look for zip files
            for path in sorted(self.config_dir.rglob("*.zip")):
                absolute = path.resolve()

                with ZipFile(absolute, "r") as zip_file:
                    for stuff in zip_file.infolist():
                        if "icon.png" in stuff.filename:
                            stuff.filename = absolute.name.replace(".zip", ".png")
                            zip_file.extract(stuff, TEMP_ICONS_DIR)

                            icon = QPixmap(str(TEMP_ICONS_DIR / stuff.filename))
                            model_items.append((True, absolute.name, icon.scaledToHeight(32)))

            self.get_configs(self.config_dir)
            for config in self.configs.values():
                if config.icon_path is not None:
                    icon = QPixmap(str(config.icon_path))
                else:
                    icon = QPixmap(str(config.default_icon_path))
                model_items.append((True, config.name, icon.scaledToHeight(32)))

            self.model_cache = [(elem[0], elem[1], elem[2]) for elem in model_items]
            self.list_configs.setModel(ListViewModel(self.model_cache))
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def btn_go_clicked(self):
        """Switches to the tracker window by hiding the main menu and creating a new tracker window for the chosen config."""

        try:
            # get selected list item infos
            index = self.list_configs.currentIndex()
            item_name: str = list(self.list_configs.model().itemData(index).values())[0]

            # extract the zip if we chose one
            if item_name.endswith(".zip"):
                zip_path = self.config_dir / item_name
                zip_file = ZipFile(zip_path)
                zip_file.extractall(TEMP_CONFIG_DIR)
                xml_path = Path(TEMP_CONFIG_DIR / "config.xml").resolve()

                self.configs[str(xml_path)] = Config(self, xml_path)

            if len(self.configs) > 0:
                self.tracker_window = TrackerWindow(self, copy(self.configs), index.row())
                self.hide()
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def action_new_triggered(self):
        """Not implemented yet. Supposed to be opening the future editor to create a new config from scratch."""
        pass

    def action_edit_triggered(self):
        """Not implemented yet. Supposed to be opening the future editor to edit an existing config."""
        pass

    def action_duplicate_triggered(self):
        """Creates a duplicate of the selected config."""

        # TODO: rename config
        config = self.get_config()
        new_config_dir = Path(str(config.config_dir))
        i = -1

        while new_config_dir.exists():
            new_config_dir = Path(str(new_config_dir) + "_copy")
            i += 1

        copytree(config.config_dir, new_config_dir)
        self.update_config_list()

    def action_delete_triggered(self):
        """Deletes the selected config."""

        config = self.get_config()

        answer = QMessageBox.question(
            self,
            "Warning",
            f"Are you sure you want to delete '{config.active_inv.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            if config.config_dir.exists():
                rmtree(config.config_dir)

            self.update_config_list()


def main():
    # argument used to display the tracker window directly, saves some time
    parser = argparse.ArgumentParser(description="Yet another randomizer item tracker.")
    parser.add_argument("--debug", "-d", dest="is_debug", action="store_true", help="debug mode")
    args = parser.parse_args()

    app = QApplication(sys.argv)

    # taskbar icon trick for Windows
    if os.name == "nt":
        from ctypes import windll

        # encoding probably useless but just in case
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

    # delete temp folder to make sure there's no unwanted files that may create conflicts
    if TEMP_DIR.exists():
        rmtree(TEMP_DIR)

    # create the temporary folders to use when working with archives
    TEMP_DIR.mkdir()
    TEMP_ICONS_DIR.mkdir()
    TEMP_CONFIG_DIR.mkdir()

    # create main menu window and show it if applicable
    main_window = MainWindow(args.is_debug)
    if not args.is_debug:
        main_window.show()

    sys.exit(app.exec())


# start the app
if __name__ == "__main__":
    main()
