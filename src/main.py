#!/usr/bin/env python3

from PyQt6 import QtWidgets, QtGui, QtCore
from sys import exit, argv
from os import name as osName
from PIL import Image

from config import Config, Color
from common import OutlinedLabel, Label, get_new_path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config: Config):
        """Main initialisation function"""

        super(MainWindow, self).__init__()

        # taskbar icon trick for Windows
        if osName == "nt":
            from ctypes import windll

            # encoding probably useless but just in case
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

        self.config = config
        offset = 34 if osName == "nt" else 20
        bg_path = get_new_path(f"config/oot/{self.config.inventory.background}")
        width, height = Image.open(bg_path).size
        self.resize(width, height + offset)
        self.setMinimumSize(QtCore.QSize(width, height + offset))
        self.setMaximumSize(QtCore.QSize(width, height + offset))
        self.setAutoFillBackground(False)
        self.setStyleSheet("")

        # set the windows's title
        self.title = "SaucisseTracker"
        self.icon = QtGui.QIcon(get_new_path("res/icon.png", True))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        ### init background frame

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
        bg_label.setPixmap(QtGui.QPixmap(get_new_path(bg_path)))

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

    def set_tier_style(self, label_tier: OutlinedLabel, color: Color):
        tier_settings = self.config.text_settings[self.config.inventory.tier_text]
        font = self.config.fonts[tier_settings.font]

        label_tier.setScaledOutlineMode(False)
        label_tier.setOutlineThickness(2)
        label_tier.setBrush(QtGui.QColor(color.r, color.g, color.b))
        label_tier.setStyleSheet(
            f"""
                font: {'75' if tier_settings.bold else ''} {tier_settings.size}pt "{font.name}";
                color: rgb({color.r}, {color.g}, {color.b});
            """
        )

    def set_pixmap_opacity(self, label: Label, opacity: float):
        pixmap = label.pixmap().copy()
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(QtCore.QPoint(), label.pixmap())
        painter.end()
        label.setPixmap(pixmap)

    def create_labels(self):
        offset = -1 if osName == "nt" else 0
        for item in self.config.inventory.items:
            label = Label(self.centralwidget, item.index)
            label.setObjectName(f"item_{item.index}")
            label.setGeometry(QtCore.QRect(item.pos.x + offset, item.pos.y + offset, 32, 32))
            label.setText("")
            label.original_pixmap = QtGui.QPixmap(get_new_path(f"config/oot/{item.paths[0]}"))
            label.setPixmap(label.original_pixmap)
            self.set_pixmap_opacity(label, 0.75)
            label.clicked_left.connect(self.label_clicked_left)
            label.clicked_middle.connect(self.label_clicked_middle)
            label.clicked_right.connect(self.label_clicked_right)

            for tier in item.tiers:
                label_tier = OutlinedLabel(label)
                label_tier.setObjectName(f"item_{item.index}_tier_{tier}")
                label_tier.setGeometry(QtCore.QRect(0, item.pos.y, 32, 32))
                label_tier.setText("")
                self.set_tier_style(label_tier, Color(255, 255, 255))
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
                self.set_pixmap_opacity(label, 0.75)
                path_index = 0
            else:
                label_effect.setStrength(0.0)  # disable filter
                label.setPixmap(label.original_pixmap)
                path_index = label.img_index

            label.original_pixmap = QtGui.QPixmap(get_new_path(f"config/oot/{item.paths[path_index]}"))
            label.setPixmap(label.original_pixmap)

            if label.img_index < 0:
                self.set_pixmap_opacity(label, 0.75)
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
                self.set_pixmap_opacity(label, 0.75)
                label_tier.setText("")
            else:
                tier_settings = self.config.text_settings[self.config.inventory.tier_text]
                label_effect.setStrength(0.0)  # disable filter
                label.setPixmap(label.original_pixmap)
                label_tier.setText(f"{item.tiers[label.tier_index]}")

                if label.tier_index == len(item.tiers) - 1:
                    self.set_tier_style(label_tier, tier_settings.color_max)
                else:
                    self.set_tier_style(label_tier, tier_settings.color)
        else:
            if label_effect.strength() > 0.0:
                label_effect.setStrength(0.0)
                label.setPixmap(label.original_pixmap)
            else:
                label_effect.setStrength(1.0)
                self.set_pixmap_opacity(label, 0.75)

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
    mainWindow = MainWindow(Config(get_new_path("config/oot/config.xml")))

    mainWindow.show()
    exit(app.exec())
