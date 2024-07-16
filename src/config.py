from xml.etree import ElementTree as ET
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from PyQt6.QtGui import QFontDatabase

from common import Label, GLOBAL_HALF_OPACITY


@dataclass
class Color:
    r: int
    g: int
    b: int

    @staticmethod
    def unpack(value: int):
        return Color((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)

    @staticmethod
    def pack(color: "Color"):
        return ((color.r & 0xFF) << 16) | ((color.g & 0xFF) << 8) | (color.b & 0xFF)


@dataclass
class Pos:
    x: int
    y: int


@dataclass
class Font:
    index: int
    name: str
    path: Path

    def __post_init__(self):
        if self.name is None:
            raise ValueError("ERROR: the font's name is none")


@dataclass
class TextSettings:
    index: int
    name: str
    font: int
    size: float
    bold: bool
    color: Color
    color_max: Color

    def __post_init__(self):
        if self.name is None:
            raise ValueError("ERROR: the name is none")


@dataclass
class Counter:
    min: int
    max: int
    increment: int
    middle_click_increment: int
    text_settings_index: int
    pos: Pos
    width: int
    height: int
    use_wheel: bool

    def __post_init__(self):
        self.value = self.min
        self.show = False

    def incr(self, middle_click: bool):
        if self.show:
            self.value += self.middle_click_increment if middle_click else self.increment

            if self.value > self.max:
                self.show = False
        else:
            self.value = self.min
            self.show = True

    def decr(self):
        if self.show:
            self.value -= self.increment

            if self.value < self.min:
                self.show = False
        else:
            self.value = self.max
            self.show = True

    def update(self, label: Label):
        if self.show:
            label.label_effect.setStrength(0.0)  # disable filter
            label.setPixmap(label.original_pixmap)
            label.label_counter.setText(f"{self.value}")
            label.label_counter.set_text_style(self.text_settings_index, self.value == self.max, 2)
        else:
            label.label_effect.setStrength(1.0)  # enable filter
            label.set_pixmap_opacity(GLOBAL_HALF_OPACITY)
            label.label_counter.setText("")


@dataclass
class InventoryItem:
    index: int
    name: str
    paths: list[Path]
    counter: Optional[Counter]
    positions: list[Pos]
    enabled: bool
    scale_content: bool
    is_reward: bool
    flag_index: Optional[int]
    use_checkmark: bool
    use_wheel: bool


@dataclass
class RewardItem:
    name: str
    text_settings_index: int


@dataclass
class FlagItem:
    texts: list[str]
    pos: Pos
    text_settings_index: int
    hidden: bool


class Rewards:
    def __init__(self):
        self.index = 0
        self.items: list[RewardItem] = []


class Inventory:
    def __init__(self):
        self.index = int()
        self.name = str()
        self.background = Path()
        self.song_check_path: Optional[Path] = None
        self.items: list[InventoryItem] = []
        self.rewards = Rewards()

        # { item_index: { pos_index: data } }
        self.label_map: dict[int, dict[int, Label]] = {}


@dataclass
class GoModeSettings:
    pos: Pos
    hide_if_disabled: bool
    path: Path
    light_path: Optional[Path]
    light_pos: Optional[Pos]


class Config:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_dir = self.config_path.parent

        self.default_inv = 0
        self.fonts: list[Font] = []
        self.text_settings: list[TextSettings] = []
        self.flags: list[FlagItem] = []
        self.inventories: dict[int, Inventory] = {}
        self.state_path: Optional[Path] = None
        self.gomode_settings: Optional[GoModeSettings] = None

        self.label_gomode: Optional[Label] = None
        self.label_gomode_light: Optional[Label] = None

        match self.config_path.suffix:
            case ".xml":
                self.parse_xml_config()
            case _:
                raise ValueError("ERROR: the config file's format isn't supported yet.")

        self.validate()

        # register external fonts
        for font in self.fonts:
            if font.path.exists():
                QFontDatabase.addApplicationFont(str(font.path.resolve()))
            else:
                raise ValueError(f"ERROR: this font doesn't exist '{font.path}'")

        # set the active inventory from default value
        self.active_inv = self.inventories[self.default_inv]

    def get_text_settings(self, text_settings_index: int):
        return self.text_settings[text_settings_index]

    def get_font(self, text_settings: TextSettings):
        return self.fonts[text_settings.font]

    def get_color(self, text_settings: TextSettings, is_max: bool = False):
        return text_settings.color_max if is_max else text_settings.color

    def parse_bool(self, value: str):
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise ValueError(f"ERROR: unknown value '{value}'")

    def parse_pos(self, raw_pos: Optional[str], name: str, raise_error: bool):
        if raw_pos is not None:
            split = raw_pos.split(";")
            if len(split) > 2:
                raise ValueError(f"ERROR: Found more than 2 positions for '{name}'")

            return Pos(int(split[0]), int(split[1]))
        elif raise_error:
            raise ValueError(f"ERROR: missing position for '{name}'")

        return None

    def parse_path(self, raw_path: Optional[str], name: str, raise_error: bool):
        if raw_path is not None:
            return self.config_dir / raw_path
        elif raise_error:
            raise ValueError(f"ERROR: Missing path(s) for item '{name}'")

        return None

    def parse_xml_config(self):
        try:
            root = ET.parse(self.config_path).getroot()
        except:
            raise FileNotFoundError(f"ERROR: File '{self.config_path}' is missing or malformed.")

        config = root.find("Config")
        if config is None:
            raise RuntimeError("ERROR: config settings not found")

        self.default_inv = int(config.get("DefaultInventory", "0"))
        self.state_path = self.parse_path(config.get("StatePath"), "savestate path", False)

        for elem in config:
            match elem.tag:
                case "Fonts":
                    for item in elem:
                        self.fonts.append(
                            Font(
                                int(item.get("Index", "0")),
                                item.get("Name"),
                                self.parse_path(item.get("Source"), "font", True),
                            )
                        )
                case "TextSettings":
                    for item in elem:
                        self.text_settings.append(
                            TextSettings(
                                int(item.get("Index", "0")),
                                item.get("Name"),
                                int(item.get("FontIndex", "0")),
                                float(item.get("Size", "10")),
                                self.parse_bool(item.get("Bold", "False")),
                                Color.unpack(int(item.get("Color", "0x000000"), 0)),
                                Color.unpack(int(item.get("ColorMax", "0x000000"), 0)),
                            )
                        )
                case "Flags":
                    for item in elem:
                        text = item.get("Text")

                        if text is None:
                            raise ValueError(f"ERROR: Missing texts for the flag")

                        self.flags.append(
                            FlagItem(
                                text.split(";"),
                                self.parse_pos(item.get("Pos"), "flag item", True),
                                int(item.get("TextSettings", "0")),
                                self.parse_bool(item.get("Hidden", "True")),
                            )
                        )
                case "GoMode":
                    p = elem.get("Source")
                    self.gomode_settings = GoModeSettings(
                        self.parse_pos(elem.get("Pos"), "go mode", True),
                        self.parse_bool(elem.get("HideIfDisabled", "False")),
                        self.parse_path(elem.get("Source"), "go mode", True),
                        self.parse_path(elem.get("LightPath"), "go mode light", False),
                        self.parse_pos(elem.get("LightPos"), "go mode light", False),
                    )
                case "Inventory":
                    inventory = Inventory()
                    inventory.index = int(elem.get("Index", "0"))
                    inventory.name = elem.get("Name", "Unknown")
                    inventory.background = self.parse_path(elem.get("Background"), "background", True)
                    inventory.song_check_path = self.parse_path(elem.get("CheckmarkPath"), "checkmark", False)

                    for i, item in enumerate(elem.iterfind("Item")):
                        name = item.get("Name", "Unknown")
                        paths: list[Path] = []
                        positions: list[Pos] = []

                        path = self.parse_path(item.get("Source"), f"item '{name}'", False)
                        if path is not None:
                            paths.append(path)
                        else:
                            sources = item.find("Sources")
                            for sub_item in sources:
                                paths.append(self.parse_path(sub_item.get("Path"), f"item '{name}'", True))

                        if len(paths) == 0:
                            raise ValueError(f"ERROR: Missing paths for item '{name}'")

                        pos = self.parse_pos(item.get("Pos"), "inventory item", False)
                        if pos is not None:
                            positions.append(pos)
                        else:
                            pos_node = item.find("Positions")
                            for sub_item in pos_node:
                                positions.append(Pos(int(sub_item.get("X", "0")), int(sub_item.get("Y", "0"))))

                        if len(positions) == 0:
                            raise ValueError(f"ERROR: Missing positions for item '{name}'")

                        counter = None
                        c = item.find("Counter")
                        if c is not None:
                            counter = Counter(
                                int(c.get("Min", "0")),
                                int(c.get("Max", "0")),
                                int(c.get("Increment", "0")),
                                int(c.get("MiddleIncrement", "0")),
                                int(c.get("TextSettings", "0")),
                                self.parse_pos(c.get("Pos"), "counter", True),
                                int(c.get("Width")),
                                int(c.get("Height")),
                                self.parse_bool(c.get("UseWheel", "False")),
                            )

                        flag_index = item.get("FlagIndex")
                        inventory.items.append(
                            InventoryItem(
                                i,
                                name,
                                paths,
                                counter,
                                positions,
                                self.parse_bool(item.get("Enabled", "False")),
                                self.parse_bool(item.get("ScaleContent", "False")),
                                self.parse_bool(item.get("Reward", "False")),
                                int(flag_index) if flag_index is not None else None,
                                self.parse_bool(item.get("UseCheckmark", "False")),
                                self.parse_bool(item.get("UseWheel", "False")),
                            )
                        )

                    rewards = elem.find("Rewards")
                    if rewards is not None:
                        for i, item in enumerate(rewards.iterfind("Item")):
                            inventory.rewards.items.append(
                                RewardItem(
                                    item.get("Name", "Unk"),
                                    int(item.get("TextSettings", "0")),
                                )
                            )

                    self.inventories[inventory.index] = inventory
                case _:
                    raise RuntimeError(f"ERROR: unknown configuration tag: '{elem.tag}'")

    def validate(self):
        if len(self.fonts) == 0:
            raise RuntimeError("ERROR: you need at least one font")

        if len(self.text_settings) == 0:
            raise RuntimeError("ERROR: you need at least one text setting for counter display")

        for inv in self.inventories.values():
            if len(inv.items) == 0:
                raise RuntimeError(f"ERROR: there's no inventory items for inventory at index {inv.index}")

            if inv.background is None:
                raise RuntimeError(f"ERROR: the background's path is none for inventory at index {inv.index}")
