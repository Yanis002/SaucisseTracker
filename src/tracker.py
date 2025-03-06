import os
import sys
import time

from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import pyqtSignal, QFileSystemWatcher, QRect, Qt, QThread
from PyQt6.QtGui import QAction, QCloseEvent, QGuiApplication, QIcon, QKeyEvent, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QVBoxLayout,
    QWidget,
)

from common import (
    Color,
    OutlinedGraphicsTextItem,
    PixmapItem,
    Pos,
    Rotation,
    show_error,
    show_message,
    OS_MENU_OFFSET,
    CURRENT_STATE_VERSION,
)

from config import Config
from state import LabelState, State
from timer import LiveSplit


class AutosaveThread(QThread):
    def __init__(self, parent: Optional[QWidget], config: Config):
        super().__init__()

        self.setParent(parent)
        self.setTerminationEnabled(True)
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
    keyPressed = pyqtSignal()

    def __init__(self, parent: Optional[QWidget], configs: dict[str, Config], config_index: int):
        super().__init__()

        self.parent_ = parent
        self.configs = configs
        self.config_index = config_index

        self.config = list(self.configs.values())[self.config_index]
        self.bg_path = self.config.active_inv.background
        self.state = State(self.config)
        self.autoreload_enabled = True
        self.timer = LiveSplit(self.config)

        self.task_autosave = AutosaveThread(self, self.config)
        self.task_autosave.start()

        self.task_rotation = Rotation(self.config)
        self.task_rotation.positionChanged.connect(self.task_rotation_position_changed)
        self.task_rotation.start()

        self.monitor = QFileSystemWatcher([str(path) for path in self.config.config_path.parent.rglob("*")], self)
        self.monitor.fileChanged.connect(self.monitor_execute)
        self.monitor.setObjectName("configMonitor")

        # accounts for platform differences for the windows' size
        self.offset = OS_MENU_OFFSET

        # create the top menu bar
        self.create_menubar()

        # create the scene and generate the items from the config
        self.central_widget = QWidget(self)
        bg_img = QPixmap(str(self.config.active_inv.background))

        self.scene = QGraphicsScene(self.central_widget)
        self.background = self.scene.addPixmap(bg_img)

        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.ze_layout = QVBoxLayout(self.central_widget)
        self.ze_layout.setContentsMargins(0, 0, 0, 0)
        self.ze_layout.addWidget(self.view)

        self.create_items()

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("SaucisseTracker")

        icon_path = Path(str(Path(__file__).resolve().parent).removesuffix("src")).resolve() / "res/icon.png"
        self.setWindowIcon(QIcon(str(icon_path)))

        # update geometry
        self.update_window_geometry(True)

        # start centered
        qtRectangle = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.show()

    def update_window_geometry(self, is_init: bool = False):
        bg_size = self.background.pixmap().size()
        menu_height = self.menu.sizeHint().height() if self.menu.isVisible() or is_init else 0

        # set background color and remove border
        self.view.setStyleSheet(
            f"background-color: {Color.to_css(self.config.active_inv.background_color)}; border: 0px;"
        )

        # update scene geometry and ze layout's geometry
        self.scene.setSceneRect(0, 0, bg_size.width(), bg_size.height())
        self.ze_layout.setGeometry(QRect(0, 0, bg_size.width(), bg_size.height()))

        # update main window's geometry
        self.setFixedSize(bg_size.width(), bg_size.height() + menu_height)

    def update_window(self):
        # update the config
        self.configs[str(self.config.config_path)] = Config(self.config.widget, self.config.config_path)
        self.config = list(self.configs.values())[self.config_index]

        if not self.config.active_inv.background.exists():
            show_error(self, f"ERROR: the following background path does not exist: {repr(self.bg_path)}")
            return

        # clear current scene items
        self.scene.clear()
        self.config.label_gomode_light = None

        ### similar to the init function ###

        # create the new background and update the scene's geometry
        bg_img = QPixmap(str(self.config.active_inv.background))
        self.background = self.scene.addPixmap(bg_img)

        # create the new items
        self.create_items()

        # update geometry
        self.update_window_geometry()

    def set_movable(self):
        # TODO: unset flags
        for item in self.scene.items():
            if item is not self.background:
                item.setFlags(
                    QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                )

    def set_selectable(self):
        # TODO: unset flags
        for item in self.scene.items():
            if item is not self.background:
                item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def find_scene_item(self, item_index: int):
        for scene_item in self.scene.items():
            if isinstance(scene_item, PixmapItem) and scene_item.state.index == item_index:
                return scene_item
        return None

    def add_pixmap(self, pixmap: QPixmap, item_index: int, obj_name: str, default_strength: float, state: LabelState):
        new_item = PixmapItem(self.config, pixmap, item_index, obj_name, default_strength, state)
        self.scene.addItem(new_item)
        return new_item

    def add_text(self, content: str):
        new_item = QGraphicsTextItem(content)
        self.scene.addItem(new_item)
        return new_item

    def add_outline_text(
        self,
        obj_name: str,
        geometry: QRect,
        text: str,
        text_settings_index: int,
        rotation: int = 0,
        parent: Optional[QGraphicsItem] = None,
    ):
        new_item = OutlinedGraphicsTextItem.new(
            self.config, obj_name, geometry, text, text_settings_index, rotation, parent
        )
        self.scene.addItem(new_item)
        return new_item

    def create_items(self):
        offset = -1 if os.name == "nt" else 0

        # the order the scene items are created defines the "priority",
        # this means older items will be more in the background while
        # recent items will show in the foreground, hence why the
        # gomode stuff is created at the end

        active_inv = self.config.active_inv

        for i, item in enumerate(active_inv.items):
            for j, item_pos in enumerate(item.positions):
                obj_name = f"item{item.index}_pos_{j}"
                pos = Pos(item_pos.x + offset, item_pos.y + offset)

                pixmap = self.add_pixmap(
                    QPixmap(str(item.paths[0])),
                    item.index,
                    obj_name,
                    0.0 if item.enabled else 1.0,
                    LabelState(item.index, j, item.name, item),
                )
                pixmap.setPos(pos.x, pos.y)
                pixmap.state.infos.enabled = item.enabled

                # rescale to 32x32 if necessary
                # TODO: allow custom values in config files?
                if item.scale_content:
                    p = pixmap.pixmap()
                    pixmap.setScale(min(32 / p.width(), 32 / p.height()))

                if item.counter is not None:
                    pixmap.label_counter = self.add_outline_text(
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
                    pixmap.label_counter.item_pixmap = pixmap
                    pixmap.label_counter.set_max_width(f"{item.counter.max}")

                if item.is_reward:
                    reward_info = active_inv.rewards.items[pixmap.state.infos.reward_index]
                    geometry = QRect(
                        pos.x + reward_info.pos.x, pos.y + reward_info.pos.y, reward_info.width, reward_info.height
                    )

                    if item.reward_map.get(j) is not None:
                        item.reward_map[j].pos(pos.x + reward_info.pos.x, pos.y + reward_info.pos.y)
                        item.reward_map[j].setPlainText(reward_info.name)
                    else:
                        item.reward_map[j] = self.add_outline_text(
                            f"{obj_name}_reward",
                            geometry,
                            reward_info.name,
                            reward_info.text_settings_index,
                        )
                        item.reward_map[j].set_max_width(active_inv.rewards.get_longest_reward())

                    if item.reward_map[j].item_pixmap is None:
                        item.reward_map[j].item_pixmap = pixmap

                if item.extra_index is not None:
                    extra = self.config.extras.items[item.extra_index]
                    n = f"{obj_name}_extra_img"
                    pixmap.extra = self.add_pixmap(
                        QPixmap(str(extra.path)), item.index, n, 0.0, LabelState(item.index, j, n, item)
                    )
                    pixmap.extra.setPos(pos.x + extra.pos.x, pos.y + extra.pos.y)
                    pixmap.extra.setVisible(False)

                if len(self.config.flags) > 0 and item.flag_index is not None:
                    flag = self.config.flags[item.flag_index]
                    pixmap.flag = self.add_outline_text(
                        f"{obj_name}_flag",
                        QRect(pos.x + flag.pos.x, pos.y + flag.pos.y, flag.width, flag.height),
                        flag.texts[pixmap.state.infos.flag_text_index],
                        flag.text_settings_index,
                    )
                    pixmap.flag.setVisible(not flag.hidden)
                    pixmap.flag.item_pixmap = pixmap
                    pixmap.flag.set_max_width(flag.get_longest_flag())

        for item in active_inv.items:
            for static_text in item.static_texts:
                if static_text.index not in active_inv.text_map:
                    active_inv.text_map[static_text.index] = self.add_outline_text(
                        f"item{item.index}_text_{static_text.index}",
                        QRect(static_text.pos.x, static_text.pos.y, static_text.width, static_text.height),
                        static_text.content,
                        static_text.text_settings_index,
                        static_text.rotation,
                    )
                    active_inv.text_map[static_text.index].set_max_width(active_inv.get_longest_static_text(True))

        for static_text in active_inv.static_texts:
            if static_text.index not in active_inv.text_map:
                active_inv.text_map[static_text.index] = self.add_outline_text(
                    f"inventory{active_inv.index}_text_{static_text.index}",
                    QRect(static_text.pos.x, static_text.pos.y, static_text.width, static_text.height),
                    static_text.content,
                    static_text.text_settings_index,
                    static_text.rotation,
                )
                active_inv.text_map[static_text.index].set_max_width(active_inv.get_longest_static_text(False))

        if self.config.gomode_settings is not None:
            gomode_settings = self.config.gomode_settings

            if gomode_settings.light_path is not None and gomode_settings.light_pos is not None:
                pixmap = QPixmap(str(gomode_settings.light_path))
                self.config.label_gomode_light = self.add_pixmap(
                    pixmap,
                    0,
                    "label_gomode_light",
                    0.0,
                    LabelState(-1, -1, "label_gomode_light", item, is_gomode_light=True),
                )
                self.config.label_gomode_light.setPos(gomode_settings.light_pos.x, gomode_settings.light_pos.y)
                self.config.label_gomode_light.setVisible(False)
                self.config.label_gomode_light.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
                self.config.label_gomode_light.setTransformOriginPoint(pixmap.rect().center().toPointF())
                self.config.label_gomode_light.state.is_gomode_light = True

            self.config.label_gomode = self.add_pixmap(
                QPixmap(str(gomode_settings.path)),
                0,
                "label_gomode",
                1.0,
                LabelState(-1, -1, "label_gomode", item, is_gomode=True),
            )
            self.config.label_gomode.setPos(gomode_settings.pos.x, gomode_settings.pos.y)

            # extremely low opacity to workaround an issue where invisible pixmaps aren't clickable
            self.config.label_gomode.setOpacity(0.001)

            self.config.label_gomode.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
            self.config.label_gomode.state.is_gomode = True

    def monitor_execute(self, raw_path: str):
        path = Path(raw_path).resolve()

        if self.autoreload_enabled:
            if path.stem == "config":
                print("change detected", path)
                self.update_window()
        else:
            print("change detected but autoreload is disabled", path)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl + ...
            match event.key():
                case Qt.Key.Key_H:
                    self.update_menu_visibility(not self.menu.isHidden())
                case Qt.Key.Key_S:
                    # kinda hacky but whatever
                    self.file_save_triggered()
                case Qt.Key.Key_O:
                    self.file_open_triggered()
                case Qt.Key.Key_T:
                    self.timer.show()
                case Qt.Key.Key_R:
                    self.update_window()

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

        self.timer.close()

        # terminate and remove the threads
        self.task_autosave.terminate()
        self.task_rotation.terminate()
        self.task_autosave = None
        self.task_rotation = None

        if self.parent_ is not None:
            self.parent_.show()
            self.close()

    def create_menubar(self):
        self.menu = QMenuBar(parent=self)
        self.menu.setObjectName("menu")

        self.menu_file = QMenu(parent=self.menu)
        self.menu_file.setObjectName("menu_file")
        self.menu_file.setTitle("File")

        self.menu_settings = QMenu(parent=self.menu)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_settings.setTitle("Settings")

        self.action_about = QAction(parent=self.menu)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.triggered.connect(self.about_triggered)

        self.action_open = QAction(self.menu_file)
        self.action_open.setObjectName("action_open")
        self.action_open.setText("Open State (Ctrl + O)")
        self.action_open.triggered.connect(self.file_open_triggered)

        self.action_save = QAction(self.menu_file)
        self.action_save.setObjectName("action_save")
        self.action_save.setText("Save State (Ctrl + S)")
        self.action_save.triggered.connect(self.file_save_triggered)

        self.action_livesplit = QAction(parent=self.menu)
        self.action_livesplit.setObjectName("action_livesplit")
        self.action_livesplit.setText("Show Timer (Ctrl+T)")
        self.action_livesplit.triggered.connect(self.timer.show)

        self.action_close = QAction(self.menu_file)
        self.action_close.setObjectName("action_close")
        self.action_close.setText("Close (Esc.)")
        self.action_close.triggered.connect(self.file_close_triggered)

        self.action_exit = QAction(self.menu_file)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setText("Exit")
        self.action_exit.triggered.connect(self.file_exit_triggered)

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_livesplit)
        self.menu_file.addAction(self.action_close)
        self.menu_file.addAction(self.action_exit)

        self.action_autosave = QAction(self.menu_file)
        self.action_autosave.setCheckable(True)
        self.action_autosave.setObjectName("action_autosave")
        self.action_autosave.setText("Autosave (5 min)")
        self.action_autosave.triggered.connect(self.file_autosave_triggered)

        self.action_autoreload = QAction(self.menu_file)
        self.action_autoreload.setCheckable(True)
        self.action_autoreload.setChecked(self.autoreload_enabled)
        self.action_autoreload.setObjectName("action_autoreload")
        self.action_autoreload.setText("Auto-reload")
        self.action_autoreload.triggered.connect(self.file_autoreload_triggered)

        self.action_hide = QAction(self.menu_file)
        self.action_hide.setObjectName("action_hide")
        self.action_hide.setText("Hide Menu (Ctrl+H)")
        self.action_hide.triggered.connect(self.settings_hide_triggered)

        self.menu_settings.addAction(self.action_hide)
        self.menu_settings.addAction(self.action_autosave)
        self.menu_settings.addAction(self.action_autoreload)

        self.menu.addAction(self.menu_file.menuAction())
        self.menu.addAction(self.menu_settings.menuAction())
        self.menu.addAction(self.action_about)
        self.setMenuBar(self.menu)

    def update_menu_visibility(self, hide: bool):
        self.menu.setHidden(hide)
        self.update_window_geometry()

    # connections callbacks

    def file_open_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = Path(
                QFileDialog.getOpenFileName(None, "Open State File", str(Path.home()), "*.txt")[0]
            ).resolve()

        if self.config.state_path.exists():
            state_items = self.state.open()
            scene_states: list[PixmapItem] = []

            if self.state.version < CURRENT_STATE_VERSION:
                show_error(self, "This state file cannot be loaded because it's outdated.")
            else:
                for item in reversed(self.scene.items()):
                    if isinstance(item, PixmapItem):
                        scene_states.append(item)

                assert len(state_items) == len(scene_states), f"{len(state_items)}, {len(scene_states)}"

                for read, cur in zip(state_items, scene_states):
                    LabelState.copy(read, cur.state)
                    cur.apply_state()

    def file_save_triggered(self):
        if self.config.state_path is None:
            self.config.state_path = Path(
                QFileDialog.getSaveFileName(None, "Save State File", str(Path.home()), "*.txt")[0]
            ).resolve()

        if self.config.state_path.parent.exists():
            self.state.items.clear()

            for item in reversed(self.scene.items()):
                if isinstance(item, PixmapItem):
                    self.state.items.append(item.state)

                    if "Bombchu" in item.state.name:
                        pass

            self.state.save()
        else:
            show_error(self, f"ERROR: This path can't be found: {repr(self.config.state_path)}")

    def file_autosave_triggered(self):
        self.config.autosave_enabled = self.action_autosave.isChecked()
        self.task_autosave.run_ = self.config.autosave_enabled

    def file_autoreload_triggered(self):
        self.autoreload_enabled = self.action_autosave.isChecked()

    def settings_hide_triggered(self):
        self.update_menu_visibility(True)

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

    def task_rotation_position_changed(self, pos):
        # only update the rotation when it's supposed to be shown
        if self.config.label_gomode_light is not None and self.config.label_gomode_light.isVisible():
            self.config.label_gomode_light.setRotation(pos)
