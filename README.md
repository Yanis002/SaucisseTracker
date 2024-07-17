# SaucisseTracker

Work in progress item tracker for randomizers. Aims to be customizable easily with a built-in editor and import/export capabilities.

## Requirements

- Python (3.10+)
- PyQt6
- Pillow

## Features

Available:
- Use a configuration file to define the background image, the different elements of the tracker and the cosmetics
- External font support
- The windows' size is based on the background size
- Upgrade tiers available through the counter system
- Progressive items available with the source paths of an item
- Import and export the tracker's state
- Dungeon reward system
- Flag system to add extra text
- Checkmarks with right click
- Main menu where you can choose which configuration you want to use

Planned:
- Editor to make configurations easier

## Project Structure

* Files:
    - ``src/common.py``: hosts classes and functions that can be used in any other file
    - ``src/config.py``: handles reading the configuration file and storing the informations in classes
    - ``src/main.py``: the main menu and the starting point of the program
    - ``src/state.py``: handles importing and exporting savestates
    - ``src/tracker.py``: the tracker window's logic is handled there (creating and updating the window/widgets/menus)

* Folders:
    - ``res/``: the program's resources (packed when building)
    - ``config/``: the tracker's configurations data, currently only hosting one example config file (not packed when building)
    - ``.github/``: hosts the GitHub workflows (to provide automated builds and releases)
    - ``.vscode/``: settings and launch profiles for Visual Studio Code

## State File Structure

**WARNING**: do NOT edit this file manually unless you know what you're doing.

The save state file is a plain text file containing informations about how to restore the progression on the tracker.

* ``Global Settings``:
    - ``gomode_visibility``: the visibility of the "go mode"
    - ``gomode_light_visibility``: the visibility of the light effect, if used
* ``Label #XX``: the items are drawn using QLabel's pixmap, the X represent the index of the label.
    - ``pos_index``: the position index, used to know which label to update when there's multiple labels with the same index
    - ``name``: the item's name, used to determine if there's a mismatch between the configuration and the save (also useful to know what's the current label corresponding to)
    - ``enabled``: used to know if the black and white filter should be applied or not
    - ``img_index``: the index of the image, used for progressive items
    - ``counter_value``: the value of the counter, if used
    - ``counter_show``: the visibility of the counter, if used
    - ``reward_index``: the index of reward name to display
    - ``flag_index``: the index of the flag the item uses
    - ``flag_text_index``: the index of the flag's text to display
    - ``show_flag``: the visibility of the flag
    - ``show_checkmark``: the visibility of the checkmark (if used)

## Config File Structure

* ``<Config>``: declares a new config
    - ``DefaultInventory``: the index to the default inventory settings to use
    - ``StatePath``: optional, can be used to set a path to save and load the tracker's state, skips the file dialogs if used
* ``<Fonts>``: list of external fonts to use
    - ``<Item>``: an element of the list
        * ``Index``: the index of the font
        * ``Name``: the name of the font (same name as the one that shows in the font preview)
        * ``Source``: the path to the font file (.ttf/.otf)
* ``<TextSettings>``: list of text settings, controls bold, size, default/max colors and the font to use
    - ``<Item>``: an element of the list
        * ``Index``: the index of the setting
        * ``Name``: the name of the setting
        * ``FontIndex``: the font index to specify which font to use
        * ``Size``: the size of the text
        * ``Bold``: toggles bold on the text
        * ``Color``: the default color, usually white (0xFFFFFF)
        * ``ColorMax``: the color to use when reaching the maximum value (for counters for instance), usually green (0x00FF00)
        * ``OutlineThickness``: the size of the outline
* ``<Flags>``: optional, list of custom extra text to display
    - ``Text``: can be used to show an extra dungeon flag with the middle click, you can use several texts separated by a ``;`` (that's something to improve in the future™)
    - ``Pos``: can be used set the flag's position (relative to the reward icon)
    - ``TextSettings``: the index of the text setting to use for the flag
    - ``Hidden``: optional, used to set the default visibility
    - ``Width``: the width of the label
    - ``Height``: the height of the label
* ``<GoMode``: optional, configurable image to set the "go mode"
* ``<Inventory>``:
    - ``Index``: the index of the inventory
    - ``Name``: the name of the inventory configuration
    - ``Background``: the background image to use for this inventory
    - ``BackgroundColor``: the color of the background if the image has transparency
    - ``CheckmarkPath``: the checkmark image to use for this inventory
    - ``<Item>``: an element of the list
        * ``Pos``: optional if using ``<Positions>``, defines the X and Y position in the window (format: ``Pos="X;Y"``)
        * ``Name``: the name of the inventory item
        * ``Source``: optional if using ``<Sources>``, defines the path to the texture to use for this item
        * ``Enabled``: optional, can be used to enable an item by default
        * ``Reward``: optional, can be set to ``True`` to declare the item as a dungeon reward
        * ``UseCheckmark``: optional, can be set to ``True`` to draw a checkmark with the right click (used for OoT songs)
        * ``UseWheel``: optional, allows using the mouse wheel to update the items faster
        * ``<Counter>``: optional, declares a new counter for this item
            - ``TextSettings``: the index of the text setting to use for this counter
            - ``Min``: the lowest amount the counter can take
            - ``Max``: the highest amount the counter can take
            - ``Increment``: how much it's adding/substracting when the item gets updated
            - ``Pos``: position of the counter (relative to the item)
            - ``Width``: the width of the counter label
            - ``Height``: the height of the counter label
            - ``MiddleIncrement``: optional, secondary increment with the middle click
        * ``<Sources>``: optional if using ``Source``, list of texture paths
            - ``<Item>``: an element of the list
                * ``Path``: the path to the texture
        * ``<Positions>``: optional if using ``Pos``, list of positions, this will use the same set of sources to draw N items, N being the number of elements of that list
            - ``<Item>``: an element of the list
                * ``X``: the position on the X axis
                * ``Y``: the position on the Y axis
    - ``<Reward>``: dungeon reward settings
        * ``<Item>``: adds a dungeon entry
            - ``Name``: the display name of the dungeon
            - ``TextSettings``: the index of the text setting to use for the name
            - ``Pos``: position of the reward name (relative to the item)
            - ``Width``: the width of the label
            - ``Height``: the height of the label

## Creating a configuration

To create your own configuration, start by creating a directory named ``config``. For executable builds you need to place it in the folder where the executable is located, if running from source it needs to be in the same folder where the ``src`` folder is (see how this repository does this)

Next, add a subfolder in the folder you just created, the name doesn't matter. Every file in this subfolder can be named and organised like you want, the only file that requires a fixed path and name is ``config.xml``, that should be located at the top-level of the config's subfolder (example: ``config/oot/config.xml``)

See the configuration file's documentation to learn more about how to create your own configuration (manually at least), an example is provided in this repo (look inside the ``config`` folder)

The background image's width and height will be used to set the window's width and height.

## Contributing

Any help is welcome!

If you wish to add support for another file format (for config files):
- go in the ``__init__`` function of the class named ``Config`` in ``config.py``
- create a new function called ``parse_FORMAT_config``, it requires at least one parameter called ``self`` (``def parse_FORMAT_config(self)``)
- find ``match self.config_path.suffix``, then add a case with the file extension of the format you want to add (like ``.json`` or ``.yml`` for example)
- call the function you created in this new case (``self.parse_FORMAT_config()``)

## Credits

Made with ♥ by me, some concepts comes from [LinSoTracker](https://github.com/linsorak/LinSoTracker) (like the "Go Mode" thing for instance)
