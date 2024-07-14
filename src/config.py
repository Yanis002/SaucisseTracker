from xml.etree import ElementTree as ET
from dataclasses import dataclass
from typing import Optional

from PyQt6.QtWidgets import QGraphicsColorizeEffect
from PyQt6.QtGui import QFontDatabase

from common import OutlinedLabel, Label, get_new_path


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
    path: str

    def __post_init__(self):
        if self.name is None:
            raise ValueError("ERROR: the font's name is none")

        if self.path is None:
            raise ValueError("ERROR: the font's path is none")


@dataclass
class TextSettings:
    index: int
    name: str
    font: int
    size: int
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
    text_settings_index: int

    def __post_init__(self):
        self.value = self.min
        self.show = False

    def incr(self):
        if self.show:
            self.value += self.increment

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


@dataclass
class InventoryItem:
    index: int
    name: str
    paths: list[str]
    counter: Optional[Counter]
    pos: Pos
    enabled: bool


class Inventory:
    def __init__(self):
        self.index = int()
        self.name = str()
        self.background: Optional[str] = None
        self.items: list[InventoryItem] = []

        self.label_effect_map: dict[int, QGraphicsColorizeEffect] = {}
        self.label_counter_map: dict[int, OutlinedLabel] = {}
        self.label_map: dict[int, Label] = {}


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file

        self.default_inv = 0
        self.fonts: list[Font] = []
        self.text_settings: list[TextSettings] = []
        self.inventories: dict[int, Inventory] = {}
        self.state_path: Optional[str] = None

        if self.config_file.endswith(".xml"):
            self.parse_xml_config()
        else:
            raise ValueError("ERROR: the config file's format isn't supported yet.")

        self.validate()

        # register external fonts
        for font in self.fonts:
            QFontDatabase.addApplicationFont(get_new_path(f"config/oot/{font.path}"))

        # set the active inventory from default value
        self.active_inv = self.inventories[self.default_inv]

    def get_bool_from_string(self, value: str):
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise ValueError(f"ERROR: unknown value '{value}'")

    def parse_xml_config(self):
        try:
            root = ET.parse(self.config_file).getroot()
        except:
            raise FileNotFoundError(f"ERROR: File '{self.config_file}' is missing or malformed.")

        config = root.find("Config")
        if config is None:
            raise RuntimeError("ERROR: config settings not found")

        self.default_inv = int(config.get("DefaultInventory", "0"))
        self.state_path = config.get("StatePath")

        for elem in config:
            match elem.tag:
                case "Fonts":
                    for item in elem:
                        self.fonts.append(Font(int(item.get("Index", "0")), item.get("Name"), item.get("Source")))
                case "TextSettings":
                    for item in elem:
                        self.text_settings.append(
                            TextSettings(
                                int(item.get("Index", "0")),
                                item.get("Name"),
                                int(item.get("FontIndex", "0")),
                                int(item.get("Size", "10")),
                                self.get_bool_from_string(item.get("Bold", "False")),
                                Color.unpack(int(item.get("Color", "0x000000"), 0)),
                                Color.unpack(int(item.get("ColorMax", "0x000000"), 0)),
                            )
                        )
                case "Inventory":
                    inventory = Inventory()
                    inventory.index = int(elem.get("Index", "0"))
                    inventory.name = elem.get("Name", "Unknown")
                    inventory.background = elem.get("Background")

                    for i, item in enumerate(elem.iterfind("Item")):
                        name = item.get("Name", "Unknown")
                        path = item.get("Source")
                        pos = item.get("Pos")
                        paths: list[str] = []

                        if path is None:
                            sources = item.find("Sources")
                            for sub_item in sources:
                                paths.append(sub_item.get("Path"))
                        else:
                            paths.append(path)

                        if None in paths:
                            raise ValueError(f"ERROR: Missing path(s) for item '{name}'")

                        if pos is None:
                            raise ValueError(f"ERROR: Missing positions for item '{name}'")

                        pos_list = pos.split(";")
                        if len(pos_list) > 2:
                            raise ValueError(f"ERROR: Found more than 2 positions for item '{name}'")

                        counter = None
                        c = item.find("Counter")
                        if c is not None:
                            counter = Counter(
                                int(c.get("Min", "0")),
                                int(c.get("Max", "0")),
                                int(c.get("Increment", "0")),
                                int(c.get("TextSettings", "0")),
                            )

                        inventory.items.append(
                            InventoryItem(
                                i,
                                name,
                                paths,
                                counter,
                                Pos(int(pos_list[0]), int(pos_list[1])),
                                self.get_bool_from_string(item.get("Enabled", "False")),
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
