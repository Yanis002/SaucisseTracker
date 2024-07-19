from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


# to test rotating stuff easily
# from https://stackoverflow.com/a/74249310
# to change the speed you can edit thread_refresh and the speed value from the Rotation instanciation
# to change the image you can edit the path inside RotationWidget's init function


class RotationWidget(QWidget):
    position = rotation = 0

    def __init__(self, image="config/oot/light.png"):
        super().__init__()
        self.image = QPixmap(image)
        self.setFixedSize(self.image.size())
        self.transform = QTransform()
        half = self.image.size() / 2
        self.tX = half.width()
        self.tY = half.height()

    def setPosition(self, pos):
        if self.position != pos:
            self.rotation = pos - self.position
        else:
            self.rotation = 0
        self.position = pos
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.transform.translate(self.tX, self.tY)
        self.transform.rotate(self.rotation)
        self.transform.translate(-self.tX, -self.tY)
        qp.setTransform(self.transform)
        qp.drawPixmap(0, 0, self.image)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(500, 500))
        self.setStyleSheet("background-color: black")
        self.rotationWidget = RotationWidget()
        self.setCentralWidget(self.rotationWidget)

    def positionChanged(self, pos):
        self.rotationWidget.setPosition(pos)


class Rotation(QThread):
    positionChanged = pyqtSignal(object)
    delta_angle = 1
    thread_refresh = 0.001

    def __init__(self, position, speed):
        super().__init__()
        self.position = position
        self.speed = speed

    def run(self):
        while True:
            diff = self.thread_refresh * self.speed
            self.position = round((self.position + diff) % 360, 2)
            self.positionChanged.emit(self.position)
            self.msleep(int(self.thread_refresh * 1000))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    item = Rotation(0, -85)
    item.positionChanged.connect(window.positionChanged)

    window.show()
    item.start()
    app.exec()
