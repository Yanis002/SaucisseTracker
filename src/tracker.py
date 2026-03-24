import os
import sys

from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import pyqtSignal, QFileSystemWatcher, QRect, Qt, QThread, QWaitCondition, QMutex
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
    debug_print,
    OS_MENU_OFFSET,
    CURRENT_STATE_VERSION,
)

from config import Config, InventoryItem, TextItem
from state import LabelState, State
from timer import LiveSplit


class AutosaveThread(QThread):
    def __init__(self, parent: Optional[QWidget], config: Config):
        super().__init__()

        self.setParent(parent)
        self.setTerminationEnabled(True)
        self.mutex = QMutex()
        self.wait_cond = QWaitCondition()
        self.config = config
        self.do_run = True
        self.setObjectName("AutosaveThread")

    def stop(self):
        self.do_run = False
        self.wait_cond.wakeAll()
        self.quit()
        self.wait()

    def run(self):
        while self.do_run:
            self.mutex.lock()
            # every 5 minutes
            # TODO: configurable time
            self.wait_cond.wait(self.mutex, (5 * 60) * 1000)
            self.mutex.unlock()

            if self.do_run and self.config.autosave_enabled:
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

    def __init__(
        self, parent: Optional[QWidget], configs: dict[str, Config], config_index: int, is_editor: bool = False
    ):
        super().__init__()

        self.parent_ = parent
        self.configs = configs
        self.config_index = config_index
        self.is_editor = is_editor

        self.config = list(self.configs.values())[self.config_index]
        self.bg_path = self.config.active_inv.background
        self.state = State(self.config)
        self.autoreload_enabled = True
        self.timer = LiveSplit(self.config, self.is_editor)

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

        self.timer_proxy = self.scene.addWidget(None)
        self.update_timer_embed(False)

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

        # load the state if existing
        if self.config.state_path is not None:
            self.file_open_triggered()
            self.config.state_saved = True

        if not self.is_editor and self.config.show_timer:
            self.timer.show()

        self.show()

    def update_timer_embed(self, update_geo: bool, force: bool = False):
        if not self.is_editor:
            if force:
                self.timer.is_separate = not self.timer.is_separate
                self.action_timer_embed.setChecked(self.timer.is_separate)
            else:
                self.timer.is_separate = not self.action_timer_embed.isChecked()

            if self.timer.is_separate:
                self.timer_proxy.setWidget(self.timer)
                self.timer_proxy.setPos(0, self.background.pixmap().size().height())
                self.timer.menu.setHidden(True)
            else:
                self.timer_proxy.setWidget(None)
                self.timer.menu.setHidden(False)
                self.timer.hide()
                self.timer.show()

        if update_geo:
            self.update_window_geometry()

    def update_window_geometry(self, is_init: bool = False):
        bg_size = self.background.pixmap().size()
        menu_height = self.menu.sizeHint().height() if self.menu.isVisible() or is_init else 0
        timer_menu_height = self.timer.menu.sizeHint().height()
        timer_height = self.timer.height() - timer_menu_height if self.timer.is_separate and not self.is_editor else 0
        offset = 1 if os.name == "nt" else 0

        # set background color and remove border
        self.view.setStyleSheet(
            f"background-color: {Color.to_css(self.config.active_inv.background_color)}; border: 0px;"
        )

        # update scene geometry and ze layout's geometry
        self.scene.setSceneRect(0, 0, bg_size.width(), bg_size.height() + timer_height)
        self.ze_layout.setGeometry(QRect(0, 0, bg_size.width(), bg_size.height() + timer_height))

        # update main window's geometry
        self.setFixedSize(bg_size.width(), bg_size.height() + menu_height + timer_height + offset)

    def update_window(self):
        prev_title = self.windowTitle()
        self.setWindowTitle("Reloading configuration...")
        self.file_save_triggered()  # trigger a save
        self.task_rotation.pause_update = True

        if not self.is_editor:
            debug_print("parsing config...")
            # update the config
            self.configs[str(self.config.config_path)] = Config(self.config.widget, self.config.config_path)
            self.config = list(self.configs.values())[self.config_index]

        if not self.config.active_inv.background.exists():
            show_error(self, f"ERROR: the following background path does not exist: {repr(self.bg_path)}")
            return

        # clear current scene items
        debug_print("clearing scene...")
        self.scene.clear()
        self.config.label_gomode = None
        self.config.label_gomode_light = None

        ### similar to the init function ###

        # create the new background and update the scene's geometry
        debug_print("setting new background pixmap...")
        bg_img = QPixmap(str(self.config.active_inv.background))
        self.background = self.scene.addPixmap(bg_img)

        if not self.is_editor:
            debug_print("recreate livesplit widget...")
            self.timer.ls_thread.stop()
            self.timer = LiveSplit(self.config, self.is_editor)
            self.timer_proxy = self.scene.addWidget(None)
            self.update_timer_embed(False)

        # create the new items
        debug_print("creating items...")
        self.create_items()

        # update geometry
        debug_print("final tasks...")
        self.update_window_geometry()
        self.task_rotation.config = self.config
        self.task_rotation.pause_update = False
        debug_print("config reloaded!")
        self.file_open_triggered()  # restore the save
        self.setWindowTitle(prev_title)

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

    def add_pixmap(
        self,
        pixmap: QPixmap,
        item_index: int,
        obj_name: str,
        default_strength: float,
        state: LabelState,
        create_effect: bool = True,
    ):
        new_item = PixmapItem(
            self.config, pixmap, item_index, obj_name, default_strength, state, create_effect=create_effect
        )
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

    def create_extra(self, item: InventoryItem, index: int, obj_name: str, pos: Pos):
        if item.extra_index is not None:
            extra = self.config.extras.items[item.extra_index]
            n = f"{obj_name}_extra_img"
            item.pixmap_items[index].extra = self.add_pixmap(
                QPixmap(str(extra.path)),
                item.index,
                n,
                0.0,
                LabelState(item.index, index, n, item),
                create_effect=False,
            )
            item.pixmap_items[index].extra.setPos(pos.x + extra.pos.x, pos.y + extra.pos.y)
            item.pixmap_items[index].extra.setVisible(False)

    def create_flag(self, item: InventoryItem, index: int, obj_name: str, pos: Pos):
        if item.flag_index is not None:
            flag = self.config.flags[item.flag_index]
            item.pixmap_items[index].flag = self.add_outline_text(
                f"{obj_name}_flag",
                QRect(pos.x + flag.pos.x, pos.y + flag.pos.y, 0, 0),
                flag.texts[item.pixmap_items[index].state.infos.flag_text_index],
                flag.text_settings_index,
            )
            item.pixmap_items[index].flag.setVisible(not flag.hidden)
            item.pixmap_items[index].flag.item_pixmap = item.pixmap_items[index]
            item.pixmap_items[index].flag.set_max_width(flag.get_longest_flag())

    def create_reward(self, item: InventoryItem, index: int, obj_name: str, pos: Pos):
        active_inv = self.config.active_inv

        if item.is_reward:
            reward_info = active_inv.rewards.items[item.pixmap_items[index].state.infos.reward_index]

            item.reward_map[index] = self.add_outline_text(
                f"{obj_name}_reward",
                QRect(pos.x + reward_info.pos.x, pos.y + reward_info.pos.y, 0, 0),
                reward_info.name,
                reward_info.text_settings_index,
            )
            item.reward_map[index].set_max_width(active_inv.rewards.get_longest_reward())

            if item.reward_map[index].item_pixmap is None:
                item.reward_map[index].item_pixmap = item.pixmap_items[index]

    def get_item_os_offset(self):
        return -1 if os.name == "nt" else 0

    def create_item(self, item: InventoryItem, index: int, item_pos: Pos):
        offset = self.get_item_os_offset()
        pos = Pos(item_pos.x + offset, item_pos.y + offset)
        obj_name = f"item{item.index}_pos_{index}"

        item.pixmap_items.append(
            self.add_pixmap(
                QPixmap(str(item.sources[0].path)),
                item.index,
                obj_name,
                0.0 if item.enabled else 1.0,
                LabelState(item.index, index, item.name, item),
            )
        )
        item.pixmap_items[index].setPos(pos.x, pos.y)
        item.pixmap_items[index].setRotation(item.rotation)
        item.pixmap_items[index].state.infos.enabled = item.enabled

        # rescale to 32x32 if necessary
        # TODO: allow custom values in config files?
        if item.scale_content:
            p = item.pixmap_items[index].pixmap()
            item.pixmap_items[index].setScale(min(32 / p.width(), 32 / p.height()))

        if item.counter is not None:
            item.pixmap_items[index].label_counter = self.add_outline_text(
                f"{obj_name}_counter",
                QRect(pos.x + item.counter.pos.x, pos.y + item.counter.pos.y, 0, 0),
                "",
                item.counter.text_settings_index,
            )
            item.pixmap_items[index].label_counter.item_pixmap = item.pixmap_items[index]
            item.pixmap_items[index].label_counter.set_max_width(f"{item.counter.max}")

        self.create_reward(item, index, obj_name, pos)
        self.create_extra(item, index, obj_name, pos)

        if len(self.config.flags) > 0:
            self.create_flag(item, index, obj_name, pos)

    def create_gomode(self, is_visible: bool):
        if self.config.gomode_settings is not None:
            gomode_settings = self.config.gomode_settings

            if gomode_settings.light_path is not None and gomode_settings.light_pos is not None:
                if self.config.label_gomode_light is None:
                    pixmap = QPixmap(str(gomode_settings.light_path))
                    self.config.label_gomode_light = self.add_pixmap(
                        pixmap,
                        0,
                        "label_gomode_light",
                        0.0,
                        LabelState(-1, -1, "label_gomode_light", None, is_gomode_light=True),
                    )

                    self.config.label_gomode_light.setVisible(is_visible)
                    self.config.label_gomode_light.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
                    self.config.label_gomode_light.setTransformOriginPoint(pixmap.rect().center().toPointF())
                    self.config.label_gomode_light.state.is_gomode_light = True

                self.config.label_gomode_light.setPos(gomode_settings.light_pos.x, gomode_settings.light_pos.y)

            if self.config.label_gomode is None:
                self.config.label_gomode = self.add_pixmap(
                    QPixmap(str(gomode_settings.path)),
                    0,
                    "label_gomode",
                    1.0,
                    LabelState(-1, -1, "label_gomode", None, is_gomode=True),
                )
                # extremely low opacity to workaround an issue where invisible pixmaps aren't clickable
                self.config.label_gomode.setOpacity(1.0 if is_visible else 0.001)

                self.config.label_gomode.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
                self.config.label_gomode.state.is_gomode = True

            self.config.label_gomode.setPos(gomode_settings.pos.x, gomode_settings.pos.y)

    def create_static_text(self, static_text: TextItem, kind: str, index: int):
        static_text.scene_item = self.add_outline_text(
            f"{kind}{index}_text_{static_text.index}",
            QRect(static_text.pos.x, static_text.pos.y, 0, 0),
            static_text.content,
            static_text.text_settings_index,
            static_text.rotation,
        )
        static_text.scene_item.set_max_width(self.config.active_inv.get_longest_static_text(kind == "item"))

    def create_items(self):
        # the order the scene items are created defines the "priority",
        # this means older items will be more in the background while
        # recent items will show in the foreground, hence why the
        # gomode stuff is created at the end

        active_inv = self.config.active_inv

        for item in active_inv.items:
            item.pixmap_items.clear()

            for j, item_pos in enumerate(item.positions):
                self.create_item(item, j, item_pos)

        for item in active_inv.items:
            for static_text in item.static_texts:
                self.create_static_text(static_text, "item", item.index)

        for static_text in active_inv.static_texts:
            self.create_static_text(static_text, "inventory", active_inv.index)

        self.create_gomode(False)

    def monitor_execute(self, raw_path: str):
        path = Path(raw_path).resolve()

        if self.autoreload_enabled:
            if path.stem == "config":
                debug_print(f"change detected ({path})")
                self.update_window()
        else:
            debug_print(f"change detected but autoreload is disabled ({path})")

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
                    if not self.is_editor:
                        self.timer.show()
                case Qt.Key.Key_R:
                    self.update_window()
                case Qt.Key.Key_P:
                    self.update_timer_embed(True, True)

    def closeEvent(self, e: Optional[QCloseEvent]):
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
        self.task_autosave.stop()
        self.task_rotation.stop()
        self.task_autosave = None
        self.task_rotation = None

        def clear_static_texts(item_list: list[TextItem]):
            for item in item_list:
                item.scene_item = None

        # cleanup existing references
        for item in self.config.active_inv.items:
            item.reward_map.clear()
            clear_static_texts(item.static_texts)

        clear_static_texts(self.config.active_inv.static_texts)
        self.scene.clear()
        self.config.label_gomode = None
        self.config.label_gomode_light = None

        if self.parent_ is not None:
            self.parent_.show()
            self.close()

        super(QMainWindow, self).closeEvent(e)

    def create_menubar(self):
        self.menu = QMenuBar()
        self.menu.setObjectName("menu")

        self.menu_file = QMenu()
        self.menu_file.setObjectName("menu_file")
        self.menu_file.setTitle("File")

        self.menu_settings = QMenu()
        self.menu_settings.setObjectName("menu_settings")
        self.menu_settings.setTitle("Settings")

        self.menu_timer = QMenu()
        self.menu_timer.setObjectName("menu_timer")
        self.menu_timer.setTitle("LiveSplit")

        self.action_about = QAction()
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

        self.action_livesplit = QAction()
        self.action_livesplit.setObjectName("action_livesplit")
        self.action_livesplit.setText("Show Timer (Ctrl + T)")
        self.action_livesplit.triggered.connect(self.timer.show)

        self.action_timer_embed = QAction(self.menu_file)
        self.action_timer_embed.setCheckable(True)
        self.action_timer_embed.setChecked(self.timer.is_separate)
        self.action_timer_embed.setObjectName("action_timer_embed")
        self.action_timer_embed.setText("Embedded Window (Ctrl + P)")
        self.action_timer_embed.triggered.connect(self.update_timer_embed_callback)

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
        self.action_hide.setText("Hide Menu (Ctrl + H)")
        self.action_hide.triggered.connect(self.settings_hide_triggered)

        self.menu_settings.addAction(self.action_hide)
        self.menu_settings.addAction(self.action_autosave)
        self.menu_settings.addAction(self.action_autoreload)

        self.menu_timer.addAction(self.action_timer_embed)
        self.menu_timer.addAction(self.action_livesplit)
        self.menu_timer.addAction(self.timer.menu_ctrls.menuAction())
        self.menu_timer.addAction(self.timer.menu_cosmetic.menuAction())

        self.menu.addAction(self.menu_file.menuAction())
        self.menu.addAction(self.menu_settings.menuAction())
        self.menu.addAction(self.menu_timer.menuAction())
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

        if self.state.version >= CURRENT_STATE_VERSION and self.config.state_path.exists():
            state_items = self.state.open()
            scene_states: list[PixmapItem] = []

            if state_items is None or self.state.version < CURRENT_STATE_VERSION:
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

    def update_timer_embed_callback(self):
        self.update_timer_embed(True)
