#!/usr/bin/env python3

import sys
import os
import colorsys

# https://github.com/LiveSplit/livesplit-core
import lib.livesplit_core as LS

from pathlib import Path
from PyQt6.QtCore import QThread, QSize, QRect, Qt
from PyQt6.QtGui import QAction, QFontDatabase, QKeyEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QLabel, QWidget, QInputDialog

# Experimental LiveSplit-based timer for my randomizer tracker
# TODO: use the renderer from livesplit-core (I don't know how it works...)
#
# Requirements: PyQt6 and livesplit-core
# License: GPL3


# from src.common import Color
class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def unpack(value: int):
        return Color((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)

    @staticmethod
    def pack(color: "Color"):
        return ((color.r & 0xFF) << 16) | ((color.g & 0xFF) << 8) | (color.b & 0xFF)


class LiveSplitThread(QThread):
    def __init__(self, main: "LiveSplit"):
        super().__init__()
        self.run_ = True
        self.main = main
        self.full_format = False
        self.is_editor_opened = False

        self.ls_run = LS.Run.new()
        self.ls_run.set_category_name("Randomizer")
        self.ls_run.push_segment(LS.Segment.new("Seed Completed"))
        self.create_timer(self.ls_run)

    def create_timer(self, run: LS.Run):
        self.ls_timer = LS.Timer.new(run)
        assert self.ls_timer is not None

    def set_time(self, start_ms: int):
        assert start_ms >= 0
        temp_sec, ms = divmod(start_ms, 1000)
        temp_min, sec = divmod(temp_sec, 60)
        hour, min = divmod(temp_min, 60)

        ms_str = f"{ms}"[:2]
        if len(ms_str) < 2:
            ms_str = f"{ms:02}"

        if self.full_format:
            text = f"{hour:02}:{min:02}:{sec:02}"
        else:
            text = f"{sec}"
            if min > 0:
                text = f"{min:02}:{text}"
            if hour > 0:
                text = f"{hour:02}:{text}"

        self.main.time_lbl.setText(f"{text}.{ms_str}")

    def get_time(self):
        if not self.is_editor_opened:
            real_time = self.ls_timer.current_time().real_time()
            assert real_time is not None
            return round(real_time.total_seconds() * 1000)
        return -1

    def start_timer(self):
        if not self.is_editor_opened:
            self.ls_timer.start()

    def reset_timer(self):
        if not self.is_editor_opened:
            self.ls_timer.reset(False)

    def toggle_pause(self):
        if not self.is_editor_opened:
            self.ls_timer.toggle_pause()

    def split(self):
        if not self.is_editor_opened:
            self.ls_timer.split()

    def set_timer_offset(self, offset: str):
        self.is_editor_opened = True
        run = self.ls_timer.into_run(False)
        del self.ls_timer
        run_editor = LS.RunEditor.new(run)
        run_editor.parse_and_set_offset(offset)
        run = run_editor.close()
        self.create_timer(run)
        self.is_editor_opened = False

    def run(self):
        while self.run_:
            if not self.is_editor_opened:
                self.set_time(self.get_time())

    def stop(self):
        self.run_ = False


class LiveSplit(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_running = False
        self.is_paused = False
        self.is_stopped = False
        self.use_gradient = True
        self.offset = 34 if os.name == "nt" else 22

        # colors defined in the config file
        self.bg_color = Color(0, 0, 0)
        self.timer_color = Color(171, 171, 171)

        self.setWindowTitle("SaucisseTimer")
        self.setFixedSize(QSize(300, 55 + self.offset))
        self.setAutoFillBackground(False)
        self.setWindowIcon(QIcon(str(Path("res/icon.png").resolve())))

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            f"background-color: rgb({self.bg_color.r}, {self.bg_color.g}, {self.bg_color.b});"
        )
        self.setCentralWidget(self.centralwidget)

        self.menu = QMenuBar(parent=self)
        self.menu.setObjectName("timer_menu")

        # Controls menu
        self.menu_ctrls = QMenu(parent=self.menu)
        self.menu_ctrls.setObjectName("menu_ctrls")
        self.menu_ctrls.setTitle("Controls")

        self.start_btn = QAction(self)
        self.start_btn.setText("Start (Ctrl+S)")
        self.start_btn.triggered.connect(self.start_timer)

        self.pause_btn = QAction(self)
        self.pause_btn.setText("Pause (Ctrl+P)")
        self.pause_btn.triggered.connect(self.pause_timer)

        self.stop_btn = QAction(self)
        self.stop_btn.setText("Stop (Ctrl+E)")
        self.stop_btn.triggered.connect(self.stop_timer)

        self.set_btn = QAction(self)
        self.set_btn.setText("Set Time (Ctrl+T)")
        self.set_btn.triggered.connect(self.set_timer_offset)

        self.menu_ctrls.addAction(self.start_btn)
        self.menu_ctrls.addAction(self.pause_btn)
        self.menu_ctrls.addAction(self.stop_btn)
        self.menu_ctrls.addAction(self.set_btn)

        # Appearence menu
        self.menu_cosmetic = QMenu(parent=self.menu)
        self.menu_cosmetic.setObjectName("menu_cosmetic")
        self.menu_cosmetic.setTitle("Appearence")

        self.time_style = QAction(self)
        self.time_style.setText("Toggle Style (Ctrl+F)")
        self.time_style.triggered.connect(self.toggle_style)

        self.gradient_btn = QAction(self)
        self.gradient_btn.setText("Toggle Gradient (Ctrl+G)")
        self.gradient_btn.triggered.connect(self.toggle_gradient)

        self.hide_btn = QAction(self)
        self.hide_btn.setText("Hide Menu (Ctrl+H)")
        self.hide_btn.triggered.connect(self.hide_menu)

        self.menu_cosmetic.addAction(self.time_style)
        self.menu_cosmetic.addAction(self.gradient_btn)
        self.menu_cosmetic.addAction(self.hide_btn)

        self.menu.addAction(self.menu_ctrls.menuAction())
        self.menu.addAction(self.menu_cosmetic.menuAction())
        self.setMenuBar(self.menu)

        self.time_lbl = QLabel(self.centralwidget)
        self.time_lbl.setGeometry(QRect(0, 0, 295, 50))
        self.time_lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )
        self.time_lbl.setWordWrap(False)
        self.set_style()

        self.ls_thread = LiveSplitThread(self)
        self.ls_thread.start()
        self.ls_thread.set_time(0)

    def set_style(self):
        font = 'font: 700 40pt "LiveSplit Timer"'

        # top color
        h, s, v = colorsys.rgb_to_hsv(self.timer_color.r / 255, self.timer_color.g / 255, self.timer_color.b / 255)
        r, g, b = colorsys.hsv_to_rgb(h, s * 0.5, min((1.5 * v + 0.1), 0.8))
        col2 = Color(r * 255, g * 255, b * 255)

        # bottom color
        h, s, v = colorsys.rgb_to_hsv(self.timer_color.r / 255, self.timer_color.g / 255, self.timer_color.b / 255)
        r, g, b = colorsys.hsv_to_rgb(h, s, v * 0.9)
        col1 = Color(r * 255, g * 255, b * 255)

        if self.use_gradient:
            self.time_lbl.setStyleSheet(
                f"""
                    {font};
                    color: qlineargradient(
                        spread:pad,
                        x1:0,
                        y1:50,
                        x2:0,
                        y2:10,
                        stop:0 rgba({col1.r}, {col1.g}, {col1.b}, 255),
                        stop:1 rgba({col2.r}, {col2.g}, {col2.b}, 255)
                    );
                """
            )
        else:
            self.time_lbl.setStyleSheet(
                f"""
                    {font};
                    color: rgba({self.timer_color.r}, {self.timer_color.g}, {self.timer_color.b}, 255);
                """
            )

    def update_menu_visibility(self, hide: bool):
        offset = 0 if hide else self.offset
        self.menu.setHidden(hide)
        self.setFixedSize(QSize(300, 55 + offset))

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.ls_thread.stop()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_Escape:
            self.update_menu_visibility(False)
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl + ...
            match event.key():
                case Qt.Key.Key_S:
                    self.start_timer()
                case Qt.Key.Key_P:
                    self.pause_timer()
                case Qt.Key.Key_E:
                    self.stop_timer()
                case Qt.Key.Key_T:
                    self.set_timer_offset()
                case Qt.Key.Key_F:
                    self.toggle_style()
                case Qt.Key.Key_G:
                    self.toggle_gradient()
                case Qt.Key.Key_H:
                    self.update_menu_visibility(not self.menu.isHidden())

    def start_timer(self):
        if not self.is_running:
            self.ls_thread.start_timer()
            self.is_running = True
            self.is_paused = False
        elif self.is_stopped:
            self.ls_thread.reset_timer()
            self.is_stopped = False
            self.is_running = False
            self.is_paused = False
        elif self.is_paused:
            self.ls_thread.toggle_pause()
            self.is_paused = not self.is_paused

    def pause_timer(self):
        if self.is_running:
            self.ls_thread.toggle_pause()
            self.is_paused = not self.is_paused

    def stop_timer(self):
        if self.is_running:
            self.ls_thread.split()
            self.is_paused = False
            self.is_stopped = True

    def set_timer_offset(self):
        if not self.is_running and not self.is_paused:
            new_time, is_ok = QInputDialog.getText(self, "Set Time", "Example: 01:23:45.67")

            if is_ok and len(new_time) > 0:
                self.ls_thread.set_timer_offset(new_time)

    def toggle_style(self):
        self.ls_thread.full_format = not self.ls_thread.full_format

    def toggle_gradient(self):
        self.use_gradient = not self.use_gradient
        self.set_style()

    def hide_menu(self):
        self.update_menu_visibility(not self.menu.isHidden())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiveSplit()
    QFontDatabase.addApplicationFont("config/oot/fonts/Timer.ttf")
    window.show()
    sys.exit(app.exec())
