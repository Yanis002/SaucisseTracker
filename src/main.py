#!/usr/bin/env python3

from typing import Optional
from PyQt6 import uic, QtWidgets, QtGui, QtCore
from sys import exit, argv
from os import path, name as osName

def get_new_path(new_path: str):
    new_path = path.dirname(path.abspath(__file__)) + new_path
    if not path.isfile(new_path):
        # temp fix for executables
        new_path = new_path.replace("/..", "")
    return new_path

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """Main initialisation function"""

        super(MainWindow, self).__init__()

        # taskbar icon trick for Windows
        if osName == "nt":
            from ctypes import windll

            # encoding probably useless but just in case
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("saucisse.tracker".encode("UTF-8"))

        self.resize(335, 474)
        self.setMinimumSize(QtCore.QSize(335, 474))
        self.setMaximumSize(QtCore.QSize(335, 474))
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
        self.bg.setGeometry(QtCore.QRect(0, 0, 335, 433))
        self.bg.setMinimumSize(QtCore.QSize(335, 433))
        self.bg.setMaximumSize(QtCore.QSize(335, 433))
        self.bg.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet(
            f"""
                background-image: url({get_new_path('/../res/background.png')});
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

        ### init temp dummy label

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(114, 239, 32, 32))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(get_new_path("/../res/item.png")))
        self.label.setObjectName("label")

        self.label.mousePressEvent = self.item_update

        # black & white effect, todo find something better? idk
        self.label_effect = QtWidgets.QGraphicsColorizeEffect(self.label)
        self.label_effect.setStrength(0.0)
        self.label_effect.setColor(QtGui.QColor('black'))
        self.label.setGraphicsEffect(self.label_effect)

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

    # connections callbacks

    def item_update(self, event: Optional[QtGui.QMouseEvent]):
        if event is not None:
            match event.button():
                case QtCore.Qt.MouseButton.LeftButton | QtCore.Qt.MouseButton.RightButton:
                    if self.label_effect.strength() > 0.0:
                        self.label_effect.setStrength(0.0)
                    else:
                        self.label_effect.setStrength(1.0)

# start the app
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mainWindow = MainWindow()

    mainWindow.show()
    exit(app.exec())
