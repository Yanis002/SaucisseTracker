from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from config import Config
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
        infos: Optional[LabelStateInfos] = None,
        is_gomode: bool = False,
        is_gomode_light: bool = False,
    ):
        self.index = index
        self.pos_index = pos_index
        self.name = name
        self.is_gomode = is_gomode
        self.is_gomode_light = is_gomode_light

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
        LabelStateInfos.copy(src.infos, dst.infos)


class State:
    def __init__(self, config: Config, path: Optional[Path] = None):
        self.config = config
        self.items: list[LabelState] = []
        self.version = (0, 0)

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
        found_global_settings = False
        items: list[LabelState] = []

        for i, line in enumerate(filedata):
            line = line.strip()

            if line.startswith("State Format Version"):
                # version is always at the very end of the file so just break the loop
                version = line.split(": ")[1].split(".")
                self.version = (int(version[0]), int(version[1]))
                break

            if line == "" or i == 0:
                if found_global_settings:
                    found_global_settings = False
                else:
                    if new_state is not None:
                        items.append(new_state)
                    new_state = LabelState(0, 0, "")

                    if line == "":
                        continue

            if not found_global_settings and line.startswith("Global Settings"):
                found_global_settings = True
            else:
                if line.startswith("gomode_visibility"):
                    self.gomode_visibility = True if line.split(" = ")[1] == "True" else False
                elif line.startswith("gomode_light_visibility"):
                    self.gomode_light_visibility = True if line.split(" = ")[1] == "True" else False
                elif new_state is not None:
                    if line.startswith("Label #"):
                        new_state.index = int(line.split("#")[1].removesuffix(":"))
                    elif line != "":
                        value = line.split(" = ")[1]

                        if line.startswith("pos_index"):
                            new_state.pos_index = int(value)
                        elif line.startswith("name"):
                            new_state.name = value.removeprefix("'").removesuffix("'")
                        elif line.startswith("enabled"):
                            new_state.infos.enabled = True if value == "True" else False
                        elif line.startswith("img_index"):
                            new_state.infos.img_index = int(value)
                        elif line.startswith("counter_value"):
                            new_state.infos.counter_value = int(value)
                        elif line.startswith("counter_show"):
                            new_state.infos.counter_show = True if value == "True" else False
                        elif line.startswith("reward_index"):
                            new_state.infos.reward_index = int(value)
                        elif line.startswith("flag_index"):
                            new_state.infos.flag_index = int(value) if value != "None" else None
                        elif line.startswith("flag_text_index"):
                            new_state.infos.flag_text_index = int(value)
                        elif line.startswith("show_flag"):
                            new_state.infos.show_flag = True if value == "True" else False
                        elif line.startswith("show_extra_img"):
                            new_state.infos.show_extra_img = True if value == "True" else False

        return items

    def open(self):
        if self.path is None:
            show_error("ERROR: import path not set")

        with self.path.open("r") as file:
            filedata = file.read().removeprefix(WARNING_TEXT).split("\n")

        return self.get_states_from_file(filedata)

    def save(self):
        if self.path is None:
            show_error("ERROR: export path not set")
            return

        gomode_visibility = False
        gomode_light_visibility = False

        gomode = self.find_gomode()
        if gomode is not None:
            gomode_visibility = gomode.infos.gomode_visibility

        gomode_light = self.find_gomode_light()
        if gomode_light is not None:
            gomode_light_visibility = gomode_light.infos.gomode_light_visibility

        self.path.write_text(
            WARNING_TEXT
            + (
                "Global Settings:\n\t"
                + f"gomode_visibility = {gomode_visibility}\n\t"
                + f"gomode_light_visibility = {gomode_light_visibility}\n\n"
            )
            + "\n".join(
                f"Label #{s.index:02}:\n\t"
                + f"pos_index = {s.pos_index}\n\t"
                + f"name = '{s.name}'\n\t"
                + f"enabled = {s.infos.enabled}\n\t"
                + f"img_index = {s.infos.img_index}\n\t"
                + f"counter_value = {s.infos.counter_value}\n\t"
                + f"counter_show = {s.infos.counter_show}\n\t"
                + f"reward_index = {s.infos.reward_index}\n\t"
                + f"flag_index = {s.infos.flag_index}\n\t"
                + f"flag_text_index = {s.infos.flag_text_index}\n\t"
                + f"show_flag = {s.infos.show_flag}\n\t"
                + f"show_extra_img = {s.infos.show_extra_img}\n"
                for s in self.items
            )
            + f"\nState Format Version: {CURRENT_STATE_VERSION[0]}.{CURRENT_STATE_VERSION[1]}\n"
        )

        self.config.state_saved = True
