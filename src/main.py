#!/usr/bin/env python3

from PyQt6 import QtWidgets, QtGui, QtCore
from sys import exit, argv
from os import name as osName
from PIL import Image

from config import TrackerConfig
from common import Label, get_new_path


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
        self.icon = QtGui.QIcon(get_new_path("/../res/icon.png"))
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

            # black & white effect, todo find something better? idk, enabled by default
            label_effect = QtWidgets.QGraphicsColorizeEffect(label)
            label_effect.setStrength(1.0)
            label_effect.setColor(QtGui.QColor("black"))
            label_effect.setObjectName(f"itemfx_{item.index}")
            label.setGraphicsEffect(label_effect)

            self.config.inventory.label_map[item.index] = label_effect

    # connections callbacks

    def update_pixmap(self, label: Label, increase: bool):
        label_effect = self.config.inventory.label_map[label.index]
        item = self.config.inventory.items[label.index]
        index = 0

        if increase:
            label.img_index += 1
        else:
            label.img_index -= 1

        if label.img_index > len(item.paths) - 1:
            label.img_index = -1
        if label.img_index < -1:
            label.img_index = len(item.paths) - 1

        print(label.img_index, len(item.paths)-1)

        if label.img_index < 0:
            label_effect.setStrength(1.0) # enable filter
            index = 0
        else:
            label_effect.setStrength(0.0) # disable filter
            index = label.img_index
        label.setPixmap(QtGui.QPixmap(get_new_path(f"/../config/oot/{item.paths[index]}")))

    def label_clicked_left(self):
        label: Label = self.sender()
        self.update_pixmap(label, True)

    def label_clicked_middle(self):
        label: Label = self.sender()

    def label_clicked_right(self):
        label: Label = self.sender()
        self.update_pixmap(label, False)


# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow(TrackerConfig(get_new_path("/../config/oot/config.xml")))

    mainWindow.show()
    exit(app.exec())
