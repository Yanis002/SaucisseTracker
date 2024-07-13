# hosts the parsing process and the data organisation of the config file

from xml.etree import ElementTree as ET
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from PyQt6 import QtWidgets, QtGui, QtCore



@dataclass
class Font:
    index: int
    path: Optional[str]

@dataclass
class Color:
    index: int
    key: str
    value: str

@dataclass
class Pos:
    x: int
    y: int

@dataclass
class InventoryItem:
    index: int
    name: str
    paths: list[str]
    tiers: list[int]
    pos: Pos

@dataclass
class TrackerInfos:
    name: str

@dataclass
class TrackerCosmetics:
    fonts: list[Font]
    colors: list[Color]
    bg_path: Optional[str]

@dataclass
class TrackerInventory:
    font: int
    items: list[InventoryItem]

    def __post_init__(self):
        self.label_map: dict[int, QtWidgets.QGraphicsColorizeEffect] = {}

class TrackerConfig:
    def __init__(self, path: str):
        self.path = path
        self.infos = TrackerInfos("Unknown")
        self.cosmetics: Optional[TrackerCosmetics] = None
        self.inventory: Optional[TrackerInventory] = None

        if self.path.endswith(".xml"):
            self.parse_xml_config()
        else:
            raise ValueError("ERROR: the config file's format isn't supported yet.")

        if self.cosmetics is None or self.inventory is None:
            raise ValueError("ERROR: Malformed data.")

    def parse_xml_config(self):
        try:
            root = ET.parse(self.path).getroot()
        except:
            raise FileNotFoundError(f"ERROR: File '{self.path}' is missing or malformed.")

        cosmetic_fonts: list[Font] = []
        cosmetic_colors: list[Color] = []
        cosmetic_bg_path: Optional[str] = None

        for node in root:
            match node.tag:
                case "Informations":
                    self.infos.name = node.get("Name", "Unknown")
                case "Background" | "Fonts" | "Colors":
                    if node.tag == "Background":
                        cosmetic_bg_path = node.get("Source")
                    else:
                        for item in node:
                            index = int(item.get("Index", "-1"))
                            if node.tag == "Fonts":
                                cosmetic_fonts.append(Font(index, item.get("Source")))
                            else:
                                cosmetic_colors.append(Color(index, item.get("Key", "unk"), item.get("Value", "0x000000")))
                case "Inventory":
                    inv_items: list[InventoryItem] = []
                    for item in node:
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
                        inv_items.append(
                            InventoryItem(
                                int(item.get("Index", "-1")),
                                name,
                                paths.split(";"),
                                tiers.split(";") if tiers is not None else list(),
                                Pos(int(pos_list[0]), int(pos_list[1]))
                            )
                        )
                    self.inventory = TrackerInventory(int(node.get("Font", "-1")), inv_items)

        if cosmetic_bg_path is None:
            raise ValueError("ERROR: the background image path is None")
        self.cosmetics = TrackerCosmetics(cosmetic_fonts, cosmetic_colors, cosmetic_bg_path)
