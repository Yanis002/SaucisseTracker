import json

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING
from xml.etree import ElementTree as ET
from xml.dom import minidom as MD

from PyQt6.QtGui import QFontDatabase, QPixmap
from PyQt6.QtWidgets import QWidget

from common import (
    Color,
    OutlinedGraphicsTextItem,
    PixmapItem,
    Pos,
    show_error,
    GLOBAL_HALF_OPACITY,
    CURRENT_XML_VERSION,
    CURRENT_JSON_VERSION,
)

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
    path: Optional[Path]

    def __post_init__(self):
        self.font_id = -1

        if self.name is None:
            show_error(self.widget, "ERROR: the font's name is none")

    def to_xml(self, parent: ET.Element, index: int):
        attrib = {
            "Index": f"{index}",
            "Name": f"{self.name}",
        }

        if self.path is not None:
            attrib["Source"] = f"{self.path.relative_to(active_config_dir)}"

        return ET.SubElement(parent, "Item", attrib)

    def to_json(self):
        data = {
            "index": self.index,
            "name": self.name,
        }

        if self.path is not None:
            data["source"] = f"{self.path.relative_to(active_config_dir)}"

        return data

    @staticmethod
    def from_json(config_dir: Path, widget: QWidget, data: dict):
        return Font(widget, data["index"], data["name"], config_dir / data["source"] if "source" in data else None)


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
        attrib = {
            "Index": f"{index}",
            "Name": f"{self.name}",
            "FontIndex": f"{self.font}",
            "Size": f"{self.size}",
            "Bold": f"{self.bold}",
            "Color": f"0x{Color.pack(self.color):06X}",
            "ColorAlt": f"0x{Color.pack(self.color_alt):06X}",
            "OutlineThickness": f"{self.outline_thickness}",
        }

        if self.is_timer:
            attrib["IsTimer"] = f"{self.is_timer}"
            attrib["UseGradient"] = f"{self.use_gradient}"
            attrib["Minimal"] = f"{self.is_minimal}"

        return ET.SubElement(parent, "Item", attrib)

    def to_json(self):
        data = {
            "index": self.index,
            "name": self.name,
            "font_index": self.font,
            "size": self.size,
            "bold": self.bold,
            "color": f"0x{Color.pack(self.color):06X}",
            "color_alt": f"0x{Color.pack(self.color_alt):06X}",
            "outline_thickness": self.outline_thickness,
            "is_timer": self.is_timer,
        }

        if self.is_timer:
            data["use_gradient"] = self.use_gradient
            data["is_minimal"] = self.is_minimal

        return data

    @staticmethod
    def from_json(widget: QWidget, data: dict):
        return TextSettings(
            widget,
            data["index"],
            data["name"],
            data["font_index"],
            data["size"],
            data["bold"],
            Color.unpack(int(data["color"], base=16)),
            Color.unpack(int(data["color_alt"], base=16)),
            data["outline_thickness"],
            data["is_timer"],
            data["use_gradient"] if "use_gradient" in data else False,
            data["is_minimal"] if "is_minimal" in data else False,
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
    """

    min: int
    max: int
    increment: int
    middle_click_increment: int
    text_settings_index: int
    pos: Pos

    def __post_init__(self):
        self.value = self.min
        self.show = False

    @staticmethod
    def from_json(data: dict):
        return Counter(
            data["min"],
            data["max"],
            data["incr"],
            data["middle_incr"],
            data["txt_settings"],
            Pos.from_str(data["pos"]),
        )

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
            pixmap.label_counter.setVisible(self.show)

            if self.show:
                if pixmap.effect is not None:
                    pixmap.effect.setStrength(0.0)  # disable filter
                pixmap.setOpacity(1.0)
                pixmap.label_counter.setPlainText(f"{self.value}")
                pixmap.label_counter.set_text_style(self.text_settings_index, self.value == self.max)
            else:
                if pixmap.effect is not None:
                    pixmap.effect.setStrength(1.0)  # enable filter
                pixmap.setOpacity(GLOBAL_HALF_OPACITY)
                pixmap.label_counter.setPlainText(f"{self.min}")


@dataclass
class RewardItem:
    pos: Pos
    name: str
    text_settings_index: int

    def to_xml(self, parent: ET.Element):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Pos": self.pos.to_str(),
                "Name": f"{self.name}",
                "TextSettings": f"{self.text_settings_index}",
            },
        )

    def to_json(self):
        return {
            "pos": self.pos.to_str(),
            "name": self.name,
            "txt_settings": self.text_settings_index,
        }

    @staticmethod
    def from_json(data: dict):
        return RewardItem(Pos.from_str(data["pos"]), data["name"], data["txt_settings"])


@dataclass
class TextItem:
    index: int
    pos: Pos
    rotation: int
    content: str
    text_settings_index: int
    scene_item: Optional[OutlinedGraphicsTextItem] = None

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Text",
            {
                "Index": f"{self.index}",
                "Pos": self.pos.to_str(),
                "Rot": f"{self.rotation}",
                "Content": self.content,
                "TextSettings": f"{self.text_settings_index}",
            },
        )

    def to_json(self):
        return {
            "index": self.index,
            "pos": self.pos.to_str(),
            "rot": f"{self.rotation}",
            "content": self.content,
            "txt_settings": self.text_settings_index,
        }

    @staticmethod
    def from_json(data: dict):
        return TextItem(
            data["index"],
            Pos.from_str(data["pos"]),
            data["rot"],
            data["content"],
            data["txt_settings"],
        )


@dataclass
class SourceItem:
    name: str
    path: Path


@dataclass
class InventoryItem:
    index: int
    name: str
    sources: list[SourceItem]
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
    pixmap_items: list[PixmapItem] = field(default_factory=list)

    def update_reward(self, index: int, reward_info: RewardItem):
        pos = self.reward_map[index].item_pixmap.pos()
        self.reward_map[index].setPlainText(reward_info.name)
        self.reward_map[index].setPos(pos.x() + reward_info.pos.x, pos.y() + reward_info.pos.y)

    def to_xml(self, parent: ET.Element, index: int):
        if index != self.index:
            print(f"WARNING: '{self.__class__.__name__}' index mismatch (expected: {self.index}, current: {index})")

        item = ET.SubElement(parent, "Item")

        attrib: dict[str, str] = {"Name": self.name}

        if len(self.sources) > 0:
            if len(self.sources) == 1:
                attrib["Source"] = str(self.sources[0].path.relative_to(active_config_dir))
            else:
                sources = ET.SubElement(item, "Sources")

                for src_item in self.sources:
                    _ = ET.SubElement(sources, "Item", {"Path": f"{src_item.path.relative_to(active_config_dir)}"})

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
                    "Text",
                    {
                        "Index": f"{label.index}",
                        "Pos": label.pos.to_str(),
                        "Rot": f"{label.rotation}",
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

    def to_json(self, index: int):
        if index != self.index:
            print(f"WARNING: '{self.__class__.__name__}' index mismatch (expected: {self.index}, current: {index})")

        sources = []
        if len(self.sources) > 0:
            if len(self.sources) == 1:
                sources = [str(self.sources[0].path.relative_to(active_config_dir))]
            else:
                for src_item in self.sources:
                    sources.append(f"{src_item.path.relative_to(active_config_dir)}")

        positions = []
        if len(self.positions) > 0:
            if len(self.positions) == 1:
                positions = [self.positions[0].to_str()]
            else:
                for pos in self.positions:
                    positions.append(pos.to_str())

        texts = []
        if len(self.static_texts) > 0:
            for label in self.static_texts:
                texts.append(
                    {
                        "index": label.index,
                        "pos": label.pos.to_str(),
                        "tot": label.rotation,
                        "content": label.content,
                        "txt_settings": label.text_settings_index,
                    },
                )

        item = {
            "index": self.index,
            "name": self.name,
            "sources": sources,
            "positions": positions,
            "rot": self.rotation,
            "texts": texts,
            "enabled": self.enabled,
            "scale_content": self.scale_content,
            "is_reward": self.is_reward,
            "use_wheel": self.use_wheel,
        }

        if self.counter is not None:
            item["counter"] = {
                "min": self.counter.min,
                "max": self.counter.max,
                "incr": self.counter.increment,
                "middle_incr": self.counter.middle_click_increment,
                "txt_settings": self.counter.text_settings_index,
                "pos": self.counter.pos.to_str(),
            }

        if self.flag_index is not None:
            item["flag_index"] = self.flag_index

        if self.extra_index is not None:
            item["extra_index"] = self.extra_index

        return item

    @staticmethod
    def from_json(config_dir: Path, data: dict):
        return InventoryItem(
            data["index"],
            data["name"],
            [SourceItem(Path(path).stem, config_dir / path) for path in data["sources"]],
            Counter.from_json(data["counter"]) if "counter" in data else None,
            [Pos.from_str(pos) for pos in data["positions"]],
            data["rot"],
            data["enabled"],
            data["scale_content"],
            data["is_reward"],
            data["flag_index"] if "flag_index" in data else None,
            data["use_wheel"],
            data["extra_index"] if "extra_index" in data else None,
            [TextItem.from_json(elem) for elem in data["texts"]],
            dict(),
        )


@dataclass
class FlagItem:
    index: int
    texts: list[str]
    pos: Pos
    text_settings_index: int
    hidden: bool

    def to_xml(self, parent: ET.Element, index: int):
        return ET.SubElement(
            parent,
            "Item",
            {
                "Index": f"{self.index}",
                "Pos": self.pos.to_str(),
                "Text": f"{';'.join(self.texts)}",
                "TextSettings": f"{self.text_settings_index}",
                "Hidden": f"{self.hidden}",
            },
        )

    def to_json(self):
        return {
            "index": self.index,
            "pos": self.pos.to_str(),
            "text": f"{';'.join(self.texts)}",
            "txt_settings": self.text_settings_index,
            "hidden": self.hidden,
        }

    @staticmethod
    def from_json(data: dict):
        return FlagItem(
            data["index"], str(data["text"]).split(";"), Pos.from_str(data["pos"]), data["txt_settings"], data["hidden"]
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

    def to_xml(self, parent: ET.Element):
        rewards = ET.SubElement(parent, "Rewards")

        for reward in self.items:
            _ = reward.to_xml(rewards)

        return rewards

    def to_json(self):
        rewards = []

        for reward in self.items:
            rewards.append(reward.to_json())

        return rewards

    @staticmethod
    def from_json(elems: list):
        rewards = Rewards()

        for data in elems:
            rewards.items.append(RewardItem.from_json(data))

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

    def to_json(self):
        return {
            "index": self.index,
            "pos": self.pos.to_str(),
            "path": f"{self.path.relative_to(active_config_dir)}",
        }

    @staticmethod
    def from_json(config_dir: Path, data: dict):
        return ExtraItem(data["index"], Pos.from_str(data["pos"]), config_dir / data["path"])


@dataclass
class Extras:
    items: list[ExtraItem]

    def to_xml(self, parent: ET.Element):
        extras = ET.SubElement(parent, "Extras")

        if len(self.items) > 0:
            for i, item in enumerate(self.items):
                _ = item.to_xml(extras)

        return extras

    def to_json(self):
        extras = []

        if len(self.items) > 0:
            for item in self.items:
                extras.append(item.to_json())

        return extras

    @staticmethod
    def from_json(config_dir: Path, elems: list):
        items = []

        for data in elems:
            items.append(ExtraItem.from_json(config_dir, data))

        return Extras(items)


class Inventory:
    def __init__(
        self,
        index: int,
        name: str,
        bg_path: Path,
        bg_color: Color,
        static_texts: list[TextItem],
    ):
        self.index = index
        self.name = name
        self.background = bg_path
        self.background_color = bg_color
        self.static_texts = static_texts

        self.items: list[InventoryItem] = []
        self.rewards = Rewards()

    @staticmethod
    def empty(index: int):
        return Inventory(index, f"New Inventory ({index})", None, Color(0, 0, 0), list())

    def to_xml(self, parent: ET.Element):
        inventory = ET.SubElement(
            parent,
            "Inventory",
            {
                "Index": f"{self.index}",
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

    def to_json(self):
        texts = []
        if len(self.static_texts) > 0:
            for text in self.static_texts:
                texts.append(text.to_json())

        items = []
        if len(self.items) > 0:
            for i, item in enumerate(self.items):
                items.append(item.to_json(i))

        return {
            "index": self.index,
            "name": self.name,
            "background": f"{self.background.relative_to(active_config_dir)}",
            "background_color": f"0x{Color.pack(self.background_color):06X}",
            "texts": texts,
            "items": items,
            "rewards": self.rewards.to_json(),
        }

    @staticmethod
    def from_json(config_dir: Path, data: dict):
        inventory = Inventory(
            data["index"],
            data["name"],
            config_dir / data["background"],
            Color.unpack(int(data["background_color"], base=16)),
            [TextItem.from_json(elem) for elem in data["texts"]],
        )

        if "rewards" in data:
            inventory.rewards = Rewards.from_json(data["rewards"])

        inventory.items = [InventoryItem.from_json(config_dir, elem) for elem in data["items"]]
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

    def remove_item(self, index: int):
        self.items.pop(index)

        for item in self.items:
            if item.index > index:
                item.index -= 1

                for pixmap_item in item.pixmap_items:
                    pixmap_item.state.index = item.index


@dataclass
class GoModeSettings:
    pos: Pos
    hide_if_disabled: bool
    path: Path
    light_path: Optional[Path]
    light_pos: Optional[Pos]
    rotation_speed: int
    thread_refresh_rate: float
    use_light: bool = False

    def to_xml(self, parent: ET.Element):
        attrib = {
            "Pos": self.pos.to_str(),
            "HideIfDisabled": f"{self.hide_if_disabled}",
            "Source": f"{self.path.relative_to(active_config_dir)}",
        }

        if self.light_path is not None and self.light_pos is not None:
            attrib["UseLight"] = f"{self.use_light}"
            attrib["LightPath"] = f"{self.light_path.relative_to(active_config_dir)}"
            attrib["LightPos"] = self.light_pos.to_str()
            attrib["LightRotSpeed"] = f"{self.rotation_speed}"
            attrib["LightRotRefresh"] = f"{self.thread_refresh_rate}"

        return ET.SubElement(parent, "GoMode", attrib)

    def to_json(self):
        data = {
            "pos": self.pos.to_str(),
            "hide_if_disabled": self.hide_if_disabled,
            "source": f"{self.path.relative_to(active_config_dir)}",
            "use_light": self.use_light,
        }

        if self.light_path is not None and self.light_pos is not None:
            data["light_path"] = f"{self.light_path.relative_to(active_config_dir)}"
            data["light_pos"] = self.light_pos.to_str()
            data["light_rot_speed"] = self.rotation_speed
            data["light_rot_refresh"] = self.thread_refresh_rate

        return data

    @staticmethod
    def from_json(config_dir: Path, data: dict):
        return GoModeSettings(
            Pos.from_str(data["pos"]),
            data["hide_if_disabled"],
            config_dir / data["source"],
            data["light_path"] if "light_path" in data else None,
            Pos.from_str(data["light_pos"]) if "light_pos" in data else None,
            data["light_rot_speed"] if "light_rot_speed" in data else None,
            data["light_rot_refresh"] if "light_rot_refresh" in data else None,
            data["use_light"],
        )


class Config:
    def __init__(self, widget: QWidget, config_path: Path):
        self.widget = widget

        self.default_inv = 0
        self.show_timer = False
        self.embed_timer = False
        self.fonts: list[Font] = []
        self.text_settings: list[TextSettings] = []
        self.flags: list[FlagItem] = []
        self.inventories: dict[int, Inventory] = {}
        self.state_path: Optional[Path] = None
        self.gomode_settings: Optional[GoModeSettings] = None
        self.extras: Optional[Extras] = None
        self.state_saved = False
        self.autosave_enabled = False
        self.xml_version = (1, 0, 1)
        self.name = str()
        self.icon_path: Optional[Path] = None
        self.default_icon_path = (
            Path(str(Path(__file__).resolve().parent).removesuffix("src")).resolve() / "res" / "config_icon.png"
        )

        self.label_gomode: Optional[PixmapItem] = None
        self.label_gomode_light: Optional[PixmapItem] = None
        self.edit_menu: Optional["TrackerEditorMenu"] = None

        if config_path is None:
            return

        self.config_path = config_path
        self.config_dir = self.config_path.parent

        match self.config_path.suffix:
            case ".xml":
                self.from_xml()
            case ".json":
                self.from_json()
            case _:
                show_error(self.widget, "ERROR: the config file's format isn't supported yet.")

        # create default inventory if necessary
        if len(self.inventories) == 0:
            self.inventories[0] = Inventory.empty(0)
        else:
            # don't validate if the config is new
            self.validate()

        # register external fonts
        for font in self.fonts:
            if font.path is not None:
                if font.path.exists():
                    font.font_id = QFontDatabase.addApplicationFont(str(font.path))
                    assert font.font_id != -1, "font cannot be added"
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

        attrib = {
            "XMLVersion": ".".join(f"{elem}" for elem in CURRENT_XML_VERSION),
            "Name": self.name,
            "Icon": f"{self.icon_path.relative_to(active_config_dir)}",
            "DefaultInventory": f"{self.default_inv}",
            "ShowTimer": f"{self.show_timer}",
            "EmbedTimer": f"{self.embed_timer}",
        }

        if self.state_path is not None:
            state_path = self.state_path
            if not state_path.is_relative_to(active_config_dir):
                state_path = self.state_path.relative_to(active_config_dir)

            attrib["StatePath"] = f"{state_path}"

        config = ET.SubElement(root, "Config", attrib)

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

        self.xml_version = tuple([int(elem) for elem in xml_version])
        self.name = config.get("Name", "Unknown Config")
        self.icon_path = self.parse_path(config.get("Icon", self.default_icon_path), "config icon path", False)
        self.default_inv = int(config.get("DefaultInventory", "0"))
        self.show_timer = self.parse_bool(config.get("ShowTimer", "False"))
        self.embed_timer = self.parse_bool(config.get("EmbedTimer", "False"))

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
                                self.parse_path(item.get("Source"), "font", False),
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

                    if self.xml_version >= (1, 0, 1):
                        self.gomode_settings.use_light = self.parse_bool(elem.get("UseLight", "False"))
                    else:
                        self.gomode_settings.use_light = (
                            self.gomode_settings.light_path is not None and self.gomode_settings.light_pos is not None
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
                        text_labels,
                    )

                    for i, item in enumerate(elem.iterfind("Item")):
                        name = item.get("Name", "Unknown")
                        src_list: list[SourceItem] = []
                        positions: list[Pos] = []

                        path = self.parse_path(item.get("Source"), f"item '{name}'", False)
                        if path is not None:
                            src_list.append(SourceItem(name, path))
                        else:
                            sources = item.find("Sources")
                            for sub_item in sources:
                                path = self.parse_path(sub_item.get("Path"), f"item '{name}'", True)
                                src_list.append(SourceItem(sub_item.get("Name", f"{path.stem}{path.suffix}"), path))

                        if len(src_list) == 0:
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
                            )

                        text_labels: list[TextItem] = []
                        for j, static_label in enumerate(item.iterfind("Text")):
                            text_labels.append(
                                TextItem(
                                    self.parse_int(static_label.get("Index"), True),
                                    self.parse_pos(static_label.get("Pos"), "inventory item label", False),
                                    self.parse_int(static_label.get("Rot", "0")),
                                    static_label.get("Content", "Unset"),
                                    self.parse_int(static_label.get("TextSettings", "0")),
                                )
                            )

                        inventory.items.append(
                            InventoryItem(
                                i,
                                name,
                                src_list,
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
                                    item.get("Name", "Unk"),
                                    int(item.get("TextSettings", "0")),
                                )
                            )

                    self.inventories[inventory.index] = inventory
                case _:
                    show_error(self.widget, f"ERROR: unknown configuration tag: '{elem.tag}'")

    def to_json(self):
        global active_config_dir

        active_config_dir = self.config_dir
        root = {
            "version": ".".join(f"{elem}" for elem in CURRENT_JSON_VERSION),
            "name": self.name,
            "icon": f"{self.icon_path.relative_to(active_config_dir)}",
            "default_inventory": self.default_inv,
            "show_timer": self.show_timer,
            "embed_timer": self.embed_timer,
        }

        if self.state_path is not None:
            state_path = self.state_path
            if not state_path.is_relative_to(active_config_dir):
                state_path = self.state_path.relative_to(active_config_dir)

            root["state_path"] = f"{state_path}"

        to_export: dict[str, Any] = {
            "fonts": self.fonts,
            "text_settings": self.text_settings,
            "flags": self.flags,
            "go_mode": self.gomode_settings,
            "extras": self.extras,
        }

        for tag, data in to_export.items():
            if isinstance(data, list):
                if len(data) > 0:
                    elems = []

                    for i, item in enumerate(data):
                        if i != item.index:
                            print(
                                f"WARNING: '{item.__class__.__name__}' index mismatch (expected: {item.index}, current: {i})"
                            )

                        elems.append(item.to_json())

                    root[tag] = elems
            elif data is not None:
                root[tag] = data.to_json()

        inventories = []
        for inventory in self.inventories.values():
            inventories.append(inventory.to_json())
        root["inventories"] = inventories

        with self.config_path.with_suffix(".json").open("w") as f:
            json.dump(root, f, indent=4)

    def from_json(self):
        try:
            root = json.loads(self.config_path.read_text())
        except:
            show_error(self.widget, f"ERROR: File '{self.config_path}' is missing or malformed.")
            return

        self.xml_version = tuple([int(elem) for elem in str(root["version"]).split(".")])
        self.name = root["name"]
        self.icon_path = self.parse_path(root["icon"], "config icon path", False)
        self.default_inv = root["default_inventory"]
        self.show_timer = root["show_timer"]
        self.embed_timer = root["embed_timer"]
        self.state_path = Path(root["state_path"]).resolve() if "state_path" in root is not None else None
        self.fonts = [Font.from_json(self.config_dir, self.widget, data) for data in root["fonts"]]
        self.gomode_settings = GoModeSettings.from_json(self.config_dir, root["go_mode"]) if "go_mode" in root else None
        self.extras = Extras.from_json(self.config_dir, root["extras"]) if "extras" in root else None
        self.inventories = {i: Inventory.from_json(self.config_dir, data) for i, data in enumerate(root["inventories"])}

        if "text_settings" in root:
            self.text_settings = [TextSettings.from_json(self.widget, data) for data in root["text_settings"]]

        if "flags" in root:
            self.flags = [FlagItem.from_json(data) for data in root["flags"]]

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
