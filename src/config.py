# hosts the parsing process and the data organisation of the config file

from xml.etree import ElementTree as ET
from dataclasses import dataclass
from typing import Optional
from PyQt6 import QtWidgets, QtGui

from common import Label, get_new_path


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
class InventoryItem:
    index: int
    name: str
    paths: list[str]
    tiers: list[int]
    pos: Pos


class Inventory:
    def __init__(self):
        self.index = int()
        self.name = str()
        self.background: Optional[str] = None
        self.tier_text = int()
        self.items: list[InventoryItem] = []

        self.label_effect_map: dict[int, QtWidgets.QGraphicsColorizeEffect] = {}
        self.label_tier_map: dict[int, Label] = {}


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file

        self.default_inv = 0
        self.fonts: list[Font] = []
        self.text_settings: list[TextSettings] = []
        self.inventory = Inventory()

        if self.config_file.endswith(".xml"):
            self.parse_xml_config()
        else:
            raise ValueError("ERROR: the config file's format isn't supported yet.")

        self.validate()

        # register external fonts
        for font in self.fonts:
            QtGui.QFontDatabase.addApplicationFont(get_new_path(f"config/oot/{font.path}"))

    def parse_xml_config(self):
        try:
            root = ET.parse(self.config_file).getroot()
        except:
            raise FileNotFoundError(f"ERROR: File '{self.config_file}' is missing or malformed.")

        config = root.find("Config")
        if config is None:
            raise RuntimeError("ERROR: config settings not found")

        self.default_inv = int(config.get("DefaultInventory", "0"))

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
                                bool(item.get("Bold", "False")),
                                Color.unpack(int(item.get("Color", "0x000000"), 0)),
                                Color.unpack(int(item.get("ColorMax", "0x000000"), 0)),
                            )
                        )
                case "Inventory":
                    self.inventory.index = int(elem.get("Index", "0"))
                    self.inventory.name = elem.get("Name", "Unknown")
                    self.inventory.background = elem.get("Background")
                    self.inventory.tier_text = int(elem.get("TierText", "0"))

                    for item in elem:
                        name = item.get("Name", "Unknown")
                        paths = item.get("Sources")
                        tiers = item.get("Tiers")
                        pos = item.get("Pos")

                        if paths is None:
                            raise ValueError(f"ERROR: Missing path(s) for item '{name}'")

                        if pos is None:
                            raise ValueError(f"ERROR: Missing positions for item '{name}'")

                        pos_list = pos.split(";")
                        if len(pos_list) > 2:
                            raise ValueError(f"ERROR: Found more than 2 positions for item '{name}'")

                        self.inventory.items.append(
                            InventoryItem(
                                int(item.get("Index", "-1")),
                                name,
                                paths.split(";"),
                                tiers.split(";") if tiers is not None else list(),
                                Pos(int(pos_list[0]), int(pos_list[1])),
                            )
                        )
                case _:
                    raise RuntimeError(f"ERROR: unknown configuration tag: '{elem.tag}'")

    def validate(self):
        if len(self.fonts) == 0:
            raise RuntimeError("ERROR: you need at least one font")

        if len(self.text_settings) == 0:
            raise RuntimeError("ERROR: you need at least one text setting for tiers display")

        if len(self.inventory.items) == 0:
            raise RuntimeError("ERROR: there's no inventory items")

        if self.inventory.background is None:
            raise RuntimeError("ERROR: the background's path is none")
