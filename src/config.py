from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING
from xml.etree import ElementTree as ET
from xml.dom import minidom as MD

from PyQt6.QtGui import QFontDatabase, QPixmap
from PyQt6.QtWidgets import QWidget

from common import Color, OutlinedGraphicsTextItem, PixmapItem, Pos, show_error, GLOBAL_HALF_OPACITY

if TYPE_CHECKING:
    from editor import TrackerEditorMenu

active_config_dir: Optional[Path] = None


@dataclass
class Font:
    """Defines a font item from `<Fonts>` (or equivalents). Hosts the name of the font, the index and the path to the font file.

    XML bindings:
    - `index` -> `Index="..."`
    - `name` -> `Name="..."`
    - `path` -> `Source="..."`
    """

    widget: QWidget
    index: int
    name: str
    path: Path

    def __post_init__(self):
        if self.name is None:
            show_error(self.widget, "ERROR: the font's name is none")

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Index": f"{index}",
                "Name": f"{self.name}",
                "Source": f"{self.path.relative_to(active_config_dir)}",
            },
        )


@dataclass
class TextSettings:
    """Defines a text setting item from `<TextSettings>` (or equivalents).

    XML bindings:
    - `index` -> `Index="..."`
    - `name` -> `Name="..."`
    - `font` -> `FontIndex="..."`
    - `size` -> `Size="..."`
    - `bold` -> `Bold="..."`
    - `color` -> `Color="..."`
    - `color_alt` -> `ColorAlt="..."`

    * Optional:
        - `outline_thickness` -> `OutlineThickness="..."`
        - `is_timer` -> `IsTimer="..."`
        - `use_gradient` -> `UseGradient="..."`
        - `is_minimal` -> `Minimal="..."`
    """

    widget: QWidget
    index: int
    name: str
    font: int
    size: float
    bold: bool
    color: Color
    color_alt: Color
    outline_thickness: float
    is_timer: bool
    use_gradient: bool
    is_minimal: bool  # hh:mm:ss.ms vs ss.ms

    def __post_init__(self):
        if self.name is None:
            show_error(self.widget, "ERROR: the name is none")

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Index": f"{index}",
                "Name": f"{self.name}",
                "FontIndex": f"{self.font}",
                "Size": f"{self.size}",
                "Bold": f"{self.bold}",
                "Color": f"0x{Color.pack(self.color):06X}",
                "ColorAlt": f"0x{Color.pack(self.color_alt):06X}",
                "OutlineThickness": f"{self.outline_thickness}",
                "IsTimer": f"{self.is_timer}",
                "UseGradient": f"{self.use_gradient}",
                "Minimal": f"{self.is_minimal}",
            },
        )


@dataclass
class Counter:
    """Defines a text setting item from `<Counter>` (or equivalents).

    XML bindings:
    - `text_settings_index` -> `TextSettings="..."`
    - `min` -> `Min="..."`
    - `max` -> `Max="..."`
    - `increment` -> `Increment="..."`
    - `pos` -> `Pos="..."`
    - `width` -> `Width="..."`
    - `height` -> `Height="..."`

    * Optional:
        - `middle_click_increment` -> `MiddleIncrement="..."`
        - `use_wheel` -> `UseWheel="..."`
    """

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

    def update(self, pixmap: PixmapItem):
        if pixmap.label_counter is not None:
            if self.show:
                pixmap.effect.setStrength(0.0)  # disable filter
                pixmap.setOpacity(1.0)
                pixmap.label_counter.setPlainText(f"{self.value}")
                pixmap.label_counter.set_text_style(self.text_settings_index, self.value == self.max)
            else:
                pixmap.effect.setStrength(1.0)  # enable filter
                pixmap.setOpacity(GLOBAL_HALF_OPACITY)
                pixmap.label_counter.setPlainText("")


@dataclass
class RewardItem:
    pos: Pos
    width: int
    height: int
    name: str
    text_settings_index: int

    def to_xml(self, parent: ET.Element):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Pos": self.pos.to_str(),
                "Width": f"{self.width}",
                "Height": f"{self.height}",
                "Name": f"{self.name}",
                "TextSettings": f"{self.text_settings_index}",
            },
        )


@dataclass
class TextItem:
    index: int
    pos: Pos
    width: int
    height: int
    rotation: int
    content: str
    text_settings_index: int

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Text",
            {
                "Index": f"{self.index}",
                "Pos": self.pos.to_str(),
                "Width": f"{self.width}",
                "Height": f"{self.height}",
                "Rot": f"{self.rotation}",
                "Content": self.content,
                "TextSettings": f"{self.text_settings_index}",
            },
        )


@dataclass
class InventoryItem:
    index: int
    name: str
    paths: list[Path]
    counter: Optional[Counter]
    positions: list[Pos]
    rotation: int
    enabled: bool
    scale_content: bool
    is_reward: bool
    flag_index: Optional[int]
    use_wheel: bool
    extra_index: Optional[int]
    static_texts: list[TextItem]
    reward_map: dict[int, OutlinedGraphicsTextItem]
    pixmap_item: Optional[PixmapItem] = None

    def update_reward(self, index: int, reward_info: RewardItem):
        pos = self.reward_map[index].item_pixmap.pos()
        self.reward_map[index].setPlainText(reward_info.name)
        self.reward_map[index].setPos(pos.x() + reward_info.pos.x, pos.y() + reward_info.pos.y)

    def to_xml(self, parent: ET.Element, index: int):
        if index != self.index:
            print(f"WARNING: '{self.__class__.__name__}' index mismatch (expected: {self.index}, current: {index})")

        item = ET.SubElement(parent, "Item")

        attrib: dict[str, str] = {"Name": self.name}

        if len(self.paths) > 0:
            if len(self.paths) == 1:
                attrib["Source"] = str(self.paths[0].relative_to(active_config_dir))
            else:
                sources = ET.SubElement(item, "Sources")

                for path in self.paths:
                    _ = ET.SubElement(sources, "Item", {"Path": f"{path.relative_to(active_config_dir)}"})

        if len(self.positions) > 0:
            if len(self.positions) == 1:
                attrib["Pos"] = self.positions[0].to_str()
            else:
                positions = ET.SubElement(item, "Positions")

                for pos in self.positions:
                    _ = ET.SubElement(positions, "Item", {"X": f"{pos.x}", "Y": f"{pos.y}"})

        attrib["Rot"] = f"{self.rotation}"

        if len(self.static_texts) > 0:
            for label in self.static_texts:
                _ = ET.SubElement(
                    item,
                    "Label",
                    {
                        "Index": f"{label.index}",
                        "Pos": label.pos.to_str(),
                        "Width": f"{label.width}",
                        "Height": f"{label.height}",
                        "Content": label.content,
                        "TextSettings": f"{label.text_settings_index}",
                    },
                )

        if self.counter is not None:
            _ = ET.SubElement(
                item,
                "Counter",
                {
                    "Min": f"{self.counter.min}",
                    "Max": f"{self.counter.max}",
                    "Increment": f"{self.counter.increment}",
                    "MiddleIncrement": f"{self.counter.middle_click_increment}",
                    "TextSettings": f"{self.counter.text_settings_index}",
                    "Pos": self.counter.pos.to_str(),
                    "Width": f"{self.counter.width}",
                    "Height": f"{self.counter.height}",
                    "UseWheel": f"{self.counter.use_wheel}",
                },
            )

        if self.enabled:
            attrib["Enabled"] = "True"

        if self.scale_content:
            attrib["ScaleContent"] = "True"

        if self.is_reward:
            attrib["Reward"] = "True"

        if self.flag_index is not None:
            attrib["FlagIndex"] = f"{self.flag_index}"

        if self.use_wheel:
            attrib["UseWheel"] = "True"

        if self.extra_index is not None:
            attrib["ExtraIndex"] = f"{self.extra_index}"

        item.attrib = attrib

        return item


@dataclass
class FlagItem:
    index: int
    texts: list[str]
    pos: Pos
    text_settings_index: int
    hidden: bool
    width: int
    height: int

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Index": f"{self.index}",
                "Pos": self.pos.to_str(),
                "Width": f"{self.width}",
                "Height": f"{self.height}",
                "Text": f"{';'.join(self.texts)}",
                "TextSettings": f"{self.text_settings_index}",
                "Hidden": f"{self.hidden}",
            },
        )

    def get_longest_flag(self):
        str_max = ""
        for txt in self.texts:
            if len(str_max) < len(txt):
                str_max = txt
        return str_max


class Rewards:
    def __init__(self):
        self.index = 0
        self.items: list[RewardItem] = []
        self.use_wheel = False

    def to_xml(self, parent: ET.Element):
        rewards = ET.SubElement(parent, "Rewards", {"UseWheel": f"{self.use_wheel}"})

        for reward in self.items:
            _ = reward.to_xml(rewards)

        return rewards

    def get_longest_reward(self):
        str_max = ""
        for reward in self.items:
            if len(str_max) < len(reward.name):
                str_max = reward.name
        return str_max


@dataclass
class ExtraItem:
    index: int
    pos: Pos
    path: Path

    def to_xml(self, parent: ET.Element):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Index": f"{self.index}",
                "Pos": self.pos.to_str(),
                "Path": f"{self.path.relative_to(active_config_dir)}",
            },
        )


@dataclass
class Extras:
    items: list[ExtraItem]

    def to_xml(self, parent: ET.Element):
        extras = ET.SubElement(parent, "Extras")

        if len(self.items) > 0:
            for i, item in enumerate(self.items):
                _ = item.to_xml(extras)

        return extras


class Inventory:
    def __init__(
        self,
        index: int,
        name: str,
        bg_path: Path,
        bg_color: Color,
        icon_path: Path,
        icon: QPixmap,
        static_texts: list[TextItem],
    ):
        self.index = index
        self.name = name
        self.background = bg_path
        self.background_color = bg_color
        self.icon_path = icon_path
        self.icon = icon
        self.static_texts = static_texts

        self.items: list[InventoryItem] = []
        self.rewards = Rewards()

        # { item_index: { pos_index: data } }
        # self.label_map: dict[int, dict[int, Label]] = {}
        self.text_map: dict[int, OutlinedGraphicsTextItem] = {}

    def to_xml(self, parent: ET.Element):
        inventory = ET.SubElement(
            parent,
            "Inventory",
            {
                "Index": f"{self.index}",
                "Icon": f"{self.icon_path.relative_to(active_config_dir)}",
                "Name": f"{self.name}",
                "Background": f"{self.background.relative_to(active_config_dir)}",
                "BackgroundColor": f"0x{Color.pack(self.background_color):06X}",
            },
        )

        if len(self.static_texts) > 0:
            for i, text in enumerate(self.static_texts):
                _ = text.to_xml(inventory, i)

        if len(self.items) > 0:
            for i, item in enumerate(self.items):
                _ = item.to_xml(inventory, i)

        _ = self.rewards.to_xml(inventory)

        return inventory

    def find_item_by_index(self, index: int):
        for item in self.items:
            if index == item.index:
                return item
        return None

    def find_item_by_name(self, name: str):
        for item in self.items:
            if name == item.name:
                return item
        return None

    def find_item(self, index: int, name: str):
        result_1 = self.find_item_by_index(index)
        if result_1 is not None:
            return result_1

        result_2 = self.find_item_by_name(name)
        if result_2 is not None:
            return result_2

        return None

    def get_longest_static_text(self, is_items: bool):
        str_max = ""

        if is_items:
            for item in self.items:
                for text in item.static_texts:
                    if len(str_max) < len(text.content):
                        str_max = text.content
        else:
            for text in self.static_texts:
                if len(str_max) < len(text.content):
                    str_max = text.content
        return str_max


@dataclass
class GoModeSettings:
    pos: Pos
    hide_if_disabled: bool
    path: Path
    light_path: Optional[Path]
    light_pos: Optional[Pos]
    rotation_speed: int
    thread_refresh_rate: float

    def to_xml(self, parent: ET.Element):
        attrib = {
            "Pos": self.pos.to_str(),
            "HideIfDisabled": f"{self.hide_if_disabled}",
            "Source": f"{self.path.relative_to(active_config_dir)}",
        }

        if self.light_path is not None and self.light_pos is not None:
            attrib["LightPath"] = f"{self.light_path.relative_to(active_config_dir)}"
            attrib["LightPos"] = self.light_pos.to_str()
            attrib["LightRotSpeed"] = f"{self.rotation_speed}"
            attrib["LightRotRefresh"] = f"{self.thread_refresh_rate}"

        return ET.SubElement(parent, "GoMode", attrib)


class Config:
    def __init__(self, widget: QWidget, config_path: Path):
        self.widget = widget
        self.config_path = config_path
        self.config_dir = self.config_path.parent

        self.default_inv = 0
        self.show_timer = False
        self.fonts: list[Font] = []
        self.text_settings: list[TextSettings] = []
        self.flags: list[FlagItem] = []
        self.inventories: dict[int, Inventory] = {}
        self.state_path: Optional[Path] = None
        self.gomode_settings: Optional[GoModeSettings] = None
        self.extras: Optional[Extras] = None
        self.state_saved = False
        self.autosave_enabled = False
        self.xml_version = (0, 0)
        self.name = str()
        self.icon_path: Optional[Path] = None
        self.default_icon_path = (
            Path(str(Path(__file__).resolve().parent).removesuffix("src")).resolve() / "res/config_icon.png"
        )

        self.label_gomode: Optional[PixmapItem] = None
        self.label_gomode_light: Optional[PixmapItem] = None
        self.edit_menu: Optional["TrackerEditorMenu"] = None

        match self.config_path.suffix:
            case ".xml":
                self.from_xml()
            case _:
                show_error(self.widget, "ERROR: the config file's format isn't supported yet.")

        self.validate()

        # register external fonts
        for font in self.fonts:
            if font.path.exists():
                QFontDatabase.addApplicationFont(str(font.path))
            else:
                show_error(self.widget, f"ERROR: this font doesn't exist '{font.path}'")

        # set the active inventory from default value
        self.active_inv = self.inventories[self.default_inv]

    def get_timer_text_settings(self):
        for settings in self.text_settings:
            if settings.is_timer:
                return settings

        # default settings
        return TextSettings(
            self.widget,
            self.text_settings[-1].index + 1,
            "Default Timer Settings",
            0,
            30.0,
            True,
            Color(171, 171, 171),
            Color(0, 0, 0),
            0.0,
            True,
            True,
            True,
        )

    def get_text_settings(self, text_settings_index: int):
        return self.text_settings[text_settings_index]

    def get_font(self, text_settings: TextSettings):
        return self.fonts[text_settings.font]

    def get_color(self, text_settings: TextSettings, is_max: bool = False):
        return text_settings.color_alt if is_max else text_settings.color

    def parse_int(self, value: Optional[str], raise_error: bool = False):
        if value is not None:
            return int(value, 0)
        elif raise_error:
            show_error(self.widget, f"ERROR: there's a missing attribute.")

        return None

    def parse_bool(self, value: str):
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            show_error(self.widget, f"ERROR: unknown value '{value}'")

        return False

    def parse_pos(self, raw_pos: Optional[str], name: str, raise_error: bool):
        if raw_pos is not None:
            split = raw_pos.split(";")
            if len(split) > 2:
                show_error(self.widget, f"ERROR: Found more than 2 positions for '{name}'")

            return Pos(int(split[0]), int(split[1]))
        elif raise_error:
            show_error(self.widget, f"ERROR: missing position for '{name}'")

        return None

    def parse_path(self, raw_path: Optional[str | Path], name: str, raise_error: bool):
        if raw_path is not None:
            # str if read from xml, path if using a default value in the elem.get() function
            if isinstance(raw_path, str):
                return Path(self.config_dir / raw_path).resolve()
            else:
                return raw_path
        elif raise_error:
            show_error(self.widget, f"ERROR: Missing path(s) for item '{name}'")

        return None

    def to_xml(self):
        global active_config_dir

        active_config_dir = self.config_dir
        root = ET.Element("Root")

        state_path = self.state_path
        if not state_path.is_relative_to(active_config_dir):
            state_path = self.state_path.relative_to(active_config_dir)

        config = ET.SubElement(
            root,
            "Config",
            {
                "XMLVersion": f"{self.xml_version[0]}.{self.xml_version[1]}",
                "Name": self.name,
                "Icon": f"{self.icon_path.relative_to(active_config_dir)}",
                "DefaultInventory": f"{self.default_inv}",
                "StatePath": f"{state_path}",
                "ShowTimer": f"{self.show_timer}",
            },
        )

        to_export: dict[str, Any] = {
            "Fonts": self.fonts,
            "TextSettings": self.text_settings,
            "Flags": self.flags,
            "GoMode": self.gomode_settings,
            "Extras": self.extras,
        }

        for tag, data in to_export.items():
            if isinstance(data, list):
                if len(data) > 0:
                    elem = ET.SubElement(config, tag)

                    for i, item in enumerate(data):
                        if i != item.index:
                            print(
                                f"WARNING: '{item.__class__.__name__}' index mismatch (expected: {item.index}, current: {i})"
                            )

                        _ = item.to_xml(elem, i)
            elif data is not None:
                _ = data.to_xml(config)

        for inventory in self.inventories.values():
            _ = inventory.to_xml(config)

        xml_str = MD.parseString(ET.tostring(root)).toprettyxml(indent=" " * 4, encoding="UTF-8")
        self.config_path.write_bytes(b"\n".join([s for s in xml_str.splitlines() if s.strip()]) + b"\n")

    def from_xml(self):
        try:
            root = ET.parse(self.config_path).getroot()
        except:
            show_error(self.widget, f"ERROR: File '{self.config_path}' is missing or malformed.")
            return

        config = root.find("Config")
        if config is None:
            show_error(self.widget, "ERROR: config settings not found")

        xml_version = config.get("XMLVersion", "0.0").split(".")

        self.xml_version = (int(xml_version[0]), int(xml_version[1]))
        self.name = config.get("Name", "Unknown Config")
        self.icon_path = self.parse_path(config.get("Icon", self.default_icon_path), "config icon path", False)
        self.default_inv = int(config.get("DefaultInventory", "0"))
        self.show_timer = self.parse_bool(config.get("ShowTimer", "False"))

        p = config.get("StatePath")
        self.state_path = Path(p).resolve() if p is not None else None

        for elem in config:
            match elem.tag:
                case "Fonts":
                    for item in elem:
                        self.fonts.append(
                            Font(
                                self.widget,
                                int(item.get("Index", "0")),
                                item.get("Name"),
                                self.parse_path(item.get("Source"), "font", True),
                            )
                        )
                case "TextSettings":
                    for item in elem:
                        self.text_settings.append(
                            TextSettings(
                                self.widget,
                                int(item.get("Index", "0")),
                                item.get("Name"),
                                int(item.get("FontIndex", "0")),
                                float(item.get("Size", "10")),
                                self.parse_bool(item.get("Bold", "False")),
                                Color.unpack(int(item.get("Color", "0xFFFFFF"), 0)),
                                Color.unpack(int(item.get("ColorAlt", "0xFFFFFF"), 0)),
                                float(item.get("OutlineThickness", "0")),
                                self.parse_bool(item.get("IsTimer", "False")),
                                self.parse_bool(item.get("UseGradient", "False")),
                                self.parse_bool(item.get("Minimal", "False")),
                            )
                        )
                case "Flags":
                    for item in elem:
                        text = item.get("Text")

                        if text is None:
                            show_error(self.widget, f"ERROR: Missing texts for the flag")

                        self.flags.append(
                            FlagItem(
                                int(item.get("Index", "0")),
                                text.split(";"),
                                self.parse_pos(item.get("Pos"), "flag item", True),
                                int(item.get("TextSettings", "0")),
                                self.parse_bool(item.get("Hidden", "True")),
                                int(item.get("Width", "0")),
                                int(item.get("Height", "0")),
                            )
                        )
                case "GoMode":
                    self.gomode_settings = GoModeSettings(
                        self.parse_pos(elem.get("Pos"), "go mode", True),
                        self.parse_bool(elem.get("HideIfDisabled", "False")),
                        self.parse_path(elem.get("Source"), "go mode", True),
                        self.parse_path(elem.get("LightPath"), "go mode light", False),
                        self.parse_pos(elem.get("LightPos"), "go mode light", False),
                        int(elem.get("LightRotSpeed", "-30")),
                        float(elem.get("LightRotRefresh", "0.001")),
                    )
                case "Extras":
                    extra_items: list[ExtraItem] = []
                    for item in elem:
                        extra_items.append(
                            ExtraItem(
                                int(item.get("Index", "0")),
                                self.parse_pos(item.get("Pos"), "extras", True),
                                self.parse_path(item.get("Path"), "extras", True),
                            )
                        )
                    self.extras = Extras(extra_items)
                case "Inventory":
                    icon_path = (
                        Path(str(Path(__file__).resolve().parent).removesuffix("src")).resolve() / "res/config_icon.png"
                    )
                    path = self.parse_path(elem.get("Icon", str(icon_path)), "icon", False)

                    text_labels: list[TextItem] = []
                    for j, static_label in enumerate(elem.iterfind("Text")):
                        text_labels.append(
                            TextItem(
                                j,
                                self.parse_pos(static_label.get("Pos"), "inventory item label", False),
                                self.parse_int(static_label.get("Width"), True),
                                self.parse_int(static_label.get("Height"), True),
                                self.parse_int(static_label.get("Rot", "0")),
                                static_label.get("Content", "Unset"),
                                self.parse_int(static_label.get("TextSettings", "0")),
                            )
                        )

                    inventory = Inventory(
                        int(elem.get("Index", "0")),
                        elem.get("Name", "Unknown"),
                        self.parse_path(elem.get("Background"), "background", True),
                        Color.unpack(int(elem.get("BackgroundColor", "0x000000"), 0)),
                        path,
                        QPixmap(str(path)),
                        text_labels,
                    )

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
                            show_error(self.widget, f"ERROR: Missing paths for item '{name}'")

                        pos = self.parse_pos(item.get("Pos"), "inventory item", False)
                        if pos is not None:
                            positions.append(pos)
                        else:
                            pos_node = item.find("Positions")
                            for sub_item in pos_node:
                                positions.append(Pos(int(sub_item.get("X", "0")), int(sub_item.get("Y", "0"))))

                        if len(positions) == 0:
                            show_error(self.widget, f"ERROR: Missing positions for item '{name}'")

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

                        text_labels: list[TextItem] = []
                        for j, static_label in enumerate(item.iterfind("Text")):
                            text_labels.append(
                                TextItem(
                                    self.parse_int(static_label.get("Index"), True),
                                    self.parse_pos(static_label.get("Pos"), "inventory item label", False),
                                    self.parse_int(static_label.get("Width"), True),
                                    self.parse_int(static_label.get("Height"), True),
                                    self.parse_int(static_label.get("Rot", "0")),
                                    static_label.get("Content", "Unset"),
                                    self.parse_int(static_label.get("TextSettings", "0")),
                                )
                            )

                        inventory.items.append(
                            InventoryItem(
                                i,
                                name,
                                paths,
                                counter,
                                positions,
                                self.parse_int(item.get("Rot", "0")),
                                self.parse_bool(item.get("Enabled", "False")),
                                self.parse_bool(item.get("ScaleContent", "False")),
                                self.parse_bool(item.get("Reward", "False")),
                                self.parse_int(item.get("FlagIndex")),
                                self.parse_bool(item.get("UseWheel", "False")),
                                self.parse_int(item.get("ExtraIndex")),
                                text_labels,
                                dict(),
                            )
                        )

                    rewards = elem.find("Rewards")
                    if rewards is not None:
                        for i, item in enumerate(rewards.iterfind("Item")):
                            inventory.rewards.items.append(
                                RewardItem(
                                    self.parse_pos(item.get("Pos"), "reward", True),
                                    int(item.get("Width", "0")),
                                    int(item.get("Height", "0")),
                                    item.get("Name", "Unk"),
                                    int(item.get("TextSettings", "0")),
                                )
                            )
                        inventory.rewards.use_wheel = self.parse_bool(rewards.get("UseWheel", "False"))

                    self.inventories[inventory.index] = inventory
                case _:
                    show_error(self.widget, f"ERROR: unknown configuration tag: '{elem.tag}'")

    def validate(self):
        if len(self.fonts) == 0:
            show_error(self.widget, "ERROR: you need at least one font")

        if len(self.text_settings) == 0:
            show_error(self.widget, "ERROR: you need at least one text setting for counter display")

        for inv in self.inventories.values():
            if len(inv.items) == 0:
                show_error(self.widget, f"ERROR: there's no inventory items for inventory at index {inv.index}")

            if inv.background is None:
                show_error(self.widget, f"ERROR: the background's path is none for inventory at index {inv.index}")
