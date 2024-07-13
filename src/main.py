#!/usr/bin/env python3

from PyQt6 import QtWidgets, QtGui, QtCore
from sys import exit, argv
from os import name as osName
from PIL import Image

from config import TrackerConfig
from common import Label, get_new_path, unpack_color


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config: TrackerConfig):
        """Main initialisation function"""

        super(MainWindow, self).__init__()

        # taskbar icon trick for Windows
        if osName == "nt":
            from ctypes import windll

            # encoding probably useless but just in case
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

        self.config = config
        bg_path = get_new_path(f"/../config/oot/{self.config.cosmetics.bg_path}")
        width, height = Image.open(bg_path).size
        self.resize(width, height + 20)
        self.setMinimumSize(QtCore.QSize(width, height + 20))
        self.setMaximumSize(QtCore.QSize(width, height + 20))
        self.setAutoFillBackground(False)
        self.setStyleSheet("")

        # set the windows's title
        self.title = "SaucisseTracker"
        self.icon = QtGui.QIcon(get_new_path("/../res/icon.png", True))
        self.centralwidget = QtWidgets.QWidget(self)

        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        ### init background frame

        self.bg = QtWidgets.QFrame(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, width, height))
        self.bg.setMinimumSize(QtCore.QSize(width, height))
        self.bg.setMaximumSize(QtCore.QSize(width, height))
        self.bg.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet(
            f"""
                background-image: url({bg_path});
                background-color: rgb(0, 0, 0);
            """
        )
        self.bg.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bg.setLineWidth(1)

        self.setCentralWidget(self.centralwidget)

        ### init menu

        self.menu = QtWidgets.QMenuBar(parent=self)
        self.menu_file = QtWidgets.QMenu(parent=self.menu)
        self.menu_about = QtWidgets.QMenu(parent=self.menu)
        self.action_open = QtGui.QAction(parent=self)
        self.action_save = QtGui.QAction(parent=self)
        self.action_exit = QtGui.QAction(parent=self)

        self.menu.setGeometry(QtCore.QRect(0, 0, 335, 21))
        self.setMenuBar(self.menu)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_exit)
        self.menu.addAction(self.menu_file.menuAction())
        self.menu.addAction(self.menu_about.menuAction())

        ### set object's names

        self.centralwidget.setObjectName("centralwidget")
        self.bg.setObjectName("bg")
        self.menu.setObjectName("menu")
        self.menu_file.setObjectName("menu_file")
        self.menu_about.setObjectName("menu_about")
        self.action_open.setObjectName("action_open")
        self.action_save.setObjectName("action_save")
        self.action_exit.setObjectName("action_exit")

        ### init items

        self.create_labels()

        ### end init

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_about.setTitle(_translate("MainWindow", "About"))
        self.action_open.setText(_translate("MainWindow", "Open (Ctrl + O)"))
        self.action_save.setText(_translate("MainWindow", "Save (Ctrl + S)"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))

    def set_tier_style(self, label_tier: Label, color: int):
        r, g, b = unpack_color(color)
        label_tier.setStyleSheet(
            f"""
                font: 75 13pt "Visitor TT1 BRK";
                color: rgb({r}, {g}, {b});
            """
        )

    def create_labels(self):
        for item in self.config.inventory.items:
            label = Label(self.centralwidget, item.index)
            label.setGeometry(QtCore.QRect(item.pos.x, item.pos.y, 32, 32))
            label.setText("")
            label.setPixmap(QtGui.QPixmap(get_new_path(f"/../config/oot/{item.paths[label.img_index]}")))
            label.setObjectName(f"item_{item.index}")
            label.clicked_left.connect(self.label_clicked_left)
            label.clicked_middle.connect(self.label_clicked_middle)
            label.clicked_right.connect(self.label_clicked_right)

            if len(item.tiers) > 0:
                label_tier = Label(label, item.index)
                label_tier.setGeometry(QtCore.QRect(item.pos.x - 10, item.pos.y, 32, 32))
                label_tier.setText("")
                label.setObjectName(f"itemtier_{item.index}")
                self.set_tier_style(label_tier, 0xFFFFFF)
                self.config.inventory.label_tier_map[item.index] = label_tier

            # black & white effect, todo find something better? idk, enabled by default
            label_effect = QtWidgets.QGraphicsColorizeEffect(label)
            label_effect.setStrength(1.0)
            label_effect.setColor(QtGui.QColor("black"))
            label_effect.setObjectName(f"itemfx_{item.index}")
            label.setGraphicsEffect(label_effect)

            self.config.inventory.label_effect_map[item.index] = label_effect

    def update_label(self, label: Label, increase: bool):
        label_effect = self.config.inventory.label_effect_map[label.index]
        label_tier = self.config.inventory.label_tier_map.get(label.index)
        item = self.config.inventory.items[label.index]
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
                path_index = 0
            else:
                label_effect.setStrength(0.0)  # disable filter
                path_index = label.img_index

            label.setPixmap(QtGui.QPixmap(get_new_path(f"/../config/oot/{item.paths[path_index]}")))
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
                label_tier.setText("")
            else:
                label_effect.setStrength(0.0)  # disable filter
                label_tier.setText(f"{item.tiers[label.tier_index]}")

                if label.tier_index == len(item.tiers) - 1:
                    self.set_tier_style(label_tier, int(self.config.cosmetics.colors[1].value, 0))
                else:
                    self.set_tier_style(label_tier, int(self.config.cosmetics.colors[0].value, 0))
        else:
            if label_effect.strength() > 0.0:
                label_effect.setStrength(0.0)
            else:
                label_effect.setStrength(1.0)

    # connections callbacks

    def label_clicked_left(self):
        label: Label = self.sender()
        self.update_label(label, True)

    def label_clicked_middle(self):
        label: Label = self.sender()

    def label_clicked_right(self):
        label: Label = self.sender()
        self.update_label(label, False)


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow(TrackerConfig(get_new_path("/../config/oot/config.xml")))

    mainWindow.show()
    exit(app.exec())
