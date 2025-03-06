from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from config import Config, InventoryItem
from common import show_error, CURRENT_STATE_VERSION


WARNING_TEXT = "!" * 63 + "\n!!! WARNING: DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING !!!\n" + "!" * 63 + "\n\n"


@dataclass
class LabelStateInfos:
    img_index: int
    counter_value: int
    counter_show: bool
    enabled: bool
    reward_index: int
    flag_index: Optional[int]
    flag_text_index: int
    show_flag: bool
    show_extra_img: bool
    gomode_visibility: bool
    gomode_light_visibility: bool

    @staticmethod
    def copy(src: "LabelStateInfos", dst: "LabelStateInfos"):
        dst.img_index = src.img_index
        dst.counter_value = src.counter_value
        dst.counter_show = src.counter_show
        dst.enabled = src.enabled
        dst.reward_index = src.reward_index
        dst.flag_index = src.flag_index
        dst.flag_text_index = src.flag_text_index
        dst.show_flag = src.show_flag
        dst.show_extra_img = src.show_extra_img
        dst.gomode_visibility = src.gomode_visibility
        dst.gomode_light_visibility = src.gomode_light_visibility


class LabelState:
    def __init__(
        self,
        index: int,
        pos_index: int,
        name: str,
        item: Optional[InventoryItem],
        infos: Optional[LabelStateInfos] = None,
        is_gomode: bool = False,
        is_gomode_light: bool = False,
    ):
        self.index = index
        self.pos_index = pos_index
        self.name = name
        self.is_gomode = is_gomode
        self.is_gomode_light = is_gomode_light
        self.item = item

        if infos is not None:
            self.infos = infos
        else:
            self.infos = LabelStateInfos(-1, int(), bool(), bool(), int(), None, int(), bool(), bool(), bool(), bool())

    @staticmethod
    def copy(src: "LabelState", dst: "LabelState"):
        dst.index = src.index
        dst.pos_index = src.pos_index
        dst.name = src.name
        dst.is_gomode = src.is_gomode
        dst.is_gomode_light = src.is_gomode_light
        dst.item = src.item
        LabelStateInfos.copy(src.infos, dst.infos)

    def export(self):
        assert self.item is not None, "inventory item is required for exporting the state"

        data = [
            f"Label #{self.index:02}:",
            f"pos_index = {self.pos_index}",
            f"name = '{self.name}'",
        ]

        if self.is_gomode:
            data.append(f"is_gomode = {self.is_gomode}")

        if self.is_gomode_light:
            data.append(f"is_gomode_light = {self.is_gomode_light}")

        if self.infos.gomode_visibility:
            data.append(f"gomode_visibility = {self.infos.gomode_visibility}")

        if self.infos.gomode_light_visibility:
            data.append(f"gomode_light_visibility = {self.infos.gomode_light_visibility}")

        data.append(f"enabled = {self.infos.enabled}")

        if len(self.item.paths) > 1:
            data.append(f"img_index = {self.infos.img_index}")

        if self.item.counter is not None:
            data.extend(
                [
                    f"counter_value = {self.infos.counter_value}",
                    f"counter_show = {self.infos.counter_show}",
                ]
            )

        if self.item.is_reward:
            data.append(f"reward_index = {self.infos.reward_index}")

        if self.item.flag_index is not None:
            data.extend(
                [
                    f"flag_index = {self.infos.flag_index}",
                    f"flag_text_index = {self.infos.flag_text_index}",
                    f"show_flag = {self.infos.show_flag}",
                ]
            )

        if self.item.extra_index is not None:
            data.append(f"show_extra_img = {self.infos.show_extra_img}")

        return "\n\t".join(data) + "\n"


class State:
    def __init__(self, config: Config, path: Optional[Path] = None):
        self.config = config
        self.items: list[LabelState] = []
        self.version = CURRENT_STATE_VERSION

        if path is not None:
            self.path = path
        elif self.config.state_path is not None:
            self.path = self.config.state_path
        else:
            self.path = Path("./state.txt").resolve()

        if self.path.suffix != ".txt":
            self.path = self.path / ".txt"

    def find_gomode(self):
        for item in self.items:
            if item.is_gomode:
                return item
        return None

    def find_gomode_light(self):
        for item in self.items:
            if item.is_gomode_light:
                return item
        return None

    def get_states_from_file(self, filedata: str):
        new_state = None
        items: list[LabelState] = []

        for i, line in enumerate(filedata):
            can_add_item = True
            line = line.strip()

            if line.startswith("State Format Version"):
                # version is always at the very end of the file so just break the loop
                version = line.split(": ")[1].split(".")
                self.version = (int(version[0]), int(version[1]))
                break

            if line == "" or i == 0:
                if new_state is not None and can_add_item:
                    items.append(new_state)
                new_state = LabelState(0, 0, "", None)

                if line == "":
                    continue

            if new_state is not None:
                if line.startswith("Label #"):
                    new_state.index = int(line.split("#")[1].removesuffix(":"))
                elif line != "":
                    elem, value = line.split(" = ")

                    match elem:
                        case "pos_index":
                            new_state.pos_index = int(value)
                        case "name":
                            new_state.name = value.removeprefix("'").removesuffix("'")
                        case "is_gomode":
                            new_state.is_gomode = True if value == "True" else False
                        case "is_gomode_light":
                            new_state.is_gomode_light = True if value == "True" else False
                        case "gomode_visibility":
                            new_state.infos.gomode_visibility = True if value == "True" else False
                        case "gomode_light_visibility":
                            new_state.infos.gomode_light_visibility = True if value == "True" else False
                        case "enabled":
                            new_state.infos.enabled = True if value == "True" else False
                        case "img_index":
                            new_state.infos.img_index = int(value)
                        case "counter_value":
                            new_state.infos.counter_value = int(value)
                        case "counter_show":
                            new_state.infos.counter_show = True if value == "True" else False
                        case "reward_index":
                            new_state.infos.reward_index = int(value)
                        case "flag_index":
                            new_state.infos.flag_index = int(value) if value != "None" else None
                        case "flag_text_index":
                            new_state.infos.flag_text_index = int(value)
                        case "show_flag":
                            new_state.infos.show_flag = True if value == "True" else False
                        case "show_extra_img":
                            new_state.infos.show_extra_img = True if value == "True" else False
                        case _:
                            can_add_item = False
                else:
                    can_add_item = False
            else:
                can_add_item = False

        return items

    def open(self):
        if self.path is None:
            show_error("ERROR: import path not set")

        with self.path.open("r") as file:
            filedata = file.read().removeprefix(WARNING_TEXT).split("\n")

        if "State Format Version" not in filedata:
            self.version = (0, 0)
            return None

        return self.get_states_from_file(filedata)

    def save(self):
        if self.path is None:
            show_error("ERROR: export path not set")
            return

        self.path.write_text(
            WARNING_TEXT
            + "\n".join(s.export() for s in self.items)
            + f"\nState Format Version: {CURRENT_STATE_VERSION[0]}.{CURRENT_STATE_VERSION[1]}\n"
        )

        self.config.state_saved = True
