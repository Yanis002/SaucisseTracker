from dataclasses import dataclass
from config import Config


WARNING_TEXT = "!" * 63 + "\n!!! WARNING: DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING !!!\n" + "!" * 63 + "\n\n"


@dataclass
class LabelState:
    index: int
    name: str
    img_index: int
    tier_index: int
    enabled: bool


class State:
    def __init__(self, config: Config):
        self.config = config
        self.states: list[LabelState] = []

        if not self.config.state_path.endswith(".txt"):
            self.config.state_path = f"{self.config.state_path}.txt"

    def get_states_from_labels(self):
        for index, label in self.config.active_inv.label_map.items():
            self.states.append(
                LabelState(
                    index,
                    self.config.active_inv.items[index].name,
                    label.img_index,
                    label.tier_index,
                    self.config.active_inv.label_effect_map[index].strength() == 0.0,
                )
            )

    def get_states_from_file(self, filedata: str):
        new_state = None

        for line in filedata:
            line = line.strip()

            if line == "":
                continue

            if line.startswith("Label #"):
                if new_state is not None:
                    self.states.append(new_state)
                new_state = LabelState(int(line.split("#")[1].removesuffix(":")), "", 0, 0, False)
            else:
                if new_state is None:
                    raise RuntimeError("ERROR: something unexpected happened...")

                value = line.split(" = ")[1]

                if line.startswith("name"):
                    new_state.name = value.removeprefix("'").removesuffix("'")
                elif line.startswith("enabled"):
                    new_state.enabled = True if value == "True" else False
                elif line.startswith("img_index"):
                    new_state.img_index = int(value)
                elif line.startswith("tier_index"):
                    new_state.tier_index = int(value)

    def open(self):
        if self.config.state_path is None:
            raise RuntimeError("ERROR: import path not set")

        with open(self.config.state_path, "r") as file:
            filedata = file.read().removeprefix(WARNING_TEXT).split("\n")

        self.get_states_from_file(filedata)

        for state in self.states:
            label = self.config.active_inv.label_map[state.index]

            if label.name != state.name:
                print(f"WARNING: name mismatch! ignoring the current label... ('{label.name}', '{state.name}')")
                continue

            label.img_index = state.img_index
            label.tier_index = state.tier_index
            label.setPixmap(label.original_pixmap)

            if label.tier_index >= 0:
                item = self.config.active_inv.items[state.index]
                tier_settings = self.config.text_settings[self.config.active_inv.tier_text]
                label_tier = self.config.active_inv.label_tier_map[state.index]
                label_tier.setText(f"{item.tiers[label.tier_index]}")

                if label.tier_index == len(item.tiers) - 1:
                    label_tier.set_tier_style(self.config, tier_settings.color_max)
                else:
                    label_tier.set_tier_style(self.config, tier_settings.color)

            if not state.enabled:
                label.set_pixmap_opacity(0.75)

            self.config.active_inv.label_effect_map[state.index].setStrength(0.0 if state.enabled else 1.0)

    def save(self):
        if self.config.state_path is None:
            raise RuntimeError("ERROR: export path not set")

        self.get_states_from_labels()

        with open(self.config.state_path, "w") as file:
            file.write(
                WARNING_TEXT
                + "\n\n".join(
                    f"Label #{s.index:02}:\n\t"
                    + f"name = '{s.name}'\n\t"
                    + f"enabled = {s.enabled}\n\t"
                    + f"img_index = {s.img_index}\n\t"
                    + f"tier_index = {s.tier_index}"
                    for s in self.states
                )
                + "\n"
            )
