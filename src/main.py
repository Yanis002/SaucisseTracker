#!/usr/bin/env python3

from PyQt6 import QtWidgets, QtGui, QtCore
from sys import exit, argv
from os import name as osName
from PIL import Image

from common import OutlinedLabel, Label, get_new_path
from config import Config, Color
from state import State


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config: Config):
        super(MainWindow, self).__init__()

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

    def create_window(self, width: int, height: int):
        # accounts for platform differences for the windows' size
        offset = 34 if osName == "nt" else 20

        # initialize the window's basic informations
        self.setWindowTitle("SaucisseTracker")
        self.setWindowIcon(QtGui.QIcon(get_new_path("res/icon.png", True)))
        self.resize(width, height + offset)
        self.setMinimumSize(QtCore.QSize(width, height + offset))
        self.setMaximumSize(QtCore.QSize(width, height + offset))
        self.setAutoFillBackground(False)

        # create the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

    def create_background(self, width: int, height: int):
        self.bg = QtWidgets.QFrame(self.centralwidget)
        self.bg.setObjectName("bg")
        self.bg.setGeometry(QtCore.QRect(0, 0, width, height))
        self.bg.setMinimumSize(QtCore.QSize(width, height))
        self.bg.setMaximumSize(QtCore.QSize(width, height))
        self.bg.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.bg.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bg.setLineWidth(1)

        # for some reasons using stylesheet for bg doesn't work on windows but this does :)
        bg_label = QtWidgets.QLabel(self.bg)
        bg_label.setObjectName(f"bg_label")
        bg_label.setGeometry(QtCore.QRect(0, 0, width, height))
        bg_label.setText("")
        bg_label.setPixmap(QtGui.QPixmap(get_new_path(self.bg_path)))

    def create_menubar(self):
        self.menu = QtWidgets.QMenuBar(parent=self)
        self.menu.setObjectName("menu")
        self.menu.setGeometry(QtCore.QRect(0, 0, 335, 21))

        self.menu_file = QtWidgets.QMenu(parent=self.menu)
        self.menu_file.setObjectName("menu_file")
        self.menu_file.setTitle("File")

        self.action_about = QtGui.QAction(parent=self.menu)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.triggered.connect(self.about_triggered)

        self.action_open = QtGui.QAction(self.menu_file)
        self.action_open.setObjectName("action_open")
        self.action_open.setText("Open State")
        self.action_open.triggered.connect(self.file_open_triggered)

        self.action_save = QtGui.QAction(self.menu_file)
        self.action_save.setObjectName("action_save")
        self.action_save.setText("Save State")
        self.action_save.triggered.connect(self.file_save_triggered)

        self.action_exit = QtGui.QAction(self.menu_file)
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
        offset = -1 if osName == "nt" else 0
        for item in self.config.active_inv.items:
            label = Label(self.centralwidget, item.index, item.name)
            label.setObjectName(f"item_{item.index}")
            label.setGeometry(QtCore.QRect(item.pos.x + offset, item.pos.y + offset, 32, 32))
            label.setText("")
            label.original_pixmap = QtGui.QPixmap(get_new_path(f"config/oot/{item.paths[0]}"))
            label.setPixmap(label.original_pixmap)
            label.set_pixmap_opacity(1.0 if item.enabled else 0.75)
            label.clicked_left.connect(self.label_clicked_left)
            label.clicked_middle.connect(self.label_clicked_middle)
            label.clicked_right.connect(self.label_clicked_right)

            for tier in item.tiers:
                label_tier = OutlinedLabel(label)
                label_tier.setObjectName(f"item_{item.index}_tier_{tier}")
                label_tier.setGeometry(QtCore.QRect(0, item.pos.y, 32, 32))
                label_tier.setText("")
                label_tier.set_tier_style(self.config, Color(255, 255, 255))
                self.config.active_inv.label_tier_map[item.index] = label_tier

            # black & white effect, todo find something better? idk, enabled by default
            label_effect = QtWidgets.QGraphicsColorizeEffect(label)
            label_effect.setStrength(0.0 if item.enabled else 1.0)
            label_effect.setColor(QtGui.QColor("black"))
            label_effect.setObjectName(f"itemfx_{item.index}")
            label.setGraphicsEffect(label_effect)

            self.config.active_inv.label_effect_map[item.index] = label_effect
            self.config.active_inv.label_map[item.index] = label

    def update_label(self, label: Label, increase: bool):
        label_effect = self.config.active_inv.label_effect_map[label.index]
        label_tier = self.config.active_inv.label_tier_map.get(label.index)
        item = self.config.active_inv.items[label.index]
        path_index = 0

        if len(item.paths) > 1:
            if increase:
                label.img_index += 1
            else:
                label.img_index -= 1

            if label.img_index > len(item.paths) - 1:
                label.img_index = -1
            if label.img_index < -1:
                label.img_index = len(item.paths) - 1

            if label.img_index < 0:
                label_effect.setStrength(1.0)  # enable filter
                label.set_pixmap_opacity(0.75)
                path_index = 0
            else:
                label_effect.setStrength(0.0)  # disable filter
                label.setPixmap(label.original_pixmap)
                path_index = label.img_index

            label.original_pixmap = QtGui.QPixmap(get_new_path(f"config/oot/{item.paths[path_index]}"))
            label.setPixmap(label.original_pixmap)

            if label.img_index < 0:
                label.set_pixmap_opacity(0.75)
            else:
                label.setPixmap(label.original_pixmap)
        elif label_tier is not None:
            if increase:
                label.tier_index += 1
            else:
                label.tier_index -= 1

            if label.tier_index > len(item.tiers) - 1:
                label.tier_index = -1
            if label.tier_index < -1:
                label.tier_index = len(item.tiers) - 1

            if label.tier_index < 0:
                label_effect.setStrength(1.0)  # enable filter
                label.set_pixmap_opacity(0.75)
                label_tier.setText("")
            else:
                tier_settings = self.config.text_settings[self.config.active_inv.tier_text]
                label_effect.setStrength(0.0)  # disable filter
                label.setPixmap(label.original_pixmap)
                label_tier.setText(f"{item.tiers[label.tier_index]}")

                if label.tier_index == len(item.tiers) - 1:
                    label_tier.set_tier_style(self.config, tier_settings.color_max)
                else:
                    label_tier.set_tier_style(self.config, tier_settings.color)
        else:
            if label_effect.strength() > 0.0:
                label_effect.setStrength(0.0)
                label.setPixmap(label.original_pixmap)
            else:
                label_effect.setStrength(1.0)
                label.set_pixmap_opacity(0.75)

    # connections callbacks

    def file_open_triggered(self):
        state = State(self.config)
        state.open()

    def file_save_triggered(self):
        state = State(self.config)
        state.save()

    def file_exit_triggered(self):
        exit()

    def about_triggered(self):
        print("You triggered about")

    def label_clicked_left(self):
        label: Label = self.sender()
        self.update_label(label, True)

    def label_clicked_middle(self):
        label: Label = self.sender()

    def label_clicked_right(self):
        label: Label = self.sender()
        self.update_label(label, False)


def main():
    # taskbar icon trick for Windows
    if osName == "nt":
        from ctypes import windll

        # encoding probably useless but just in case
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow(Config(get_new_path("config/oot/config.xml")))

    mainWindow.show()
    exit(app.exec())


# start the app
if __name__ == "__main__":
    main()
