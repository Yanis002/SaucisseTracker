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

Planned:
- Editor to make configurations easier
- Reward system (like medallions and stones for OoT)

## Project Structure

* Files:
    - ``src/common.py``: hosts classes and functions that can be used in any other file
    - ``src/config.py``: handles reading the configuration file and storing the informations in classes
    - ``src/main.py``: the main window's logic is handled there (creating and updating the window/widgets/menus)

* Folders:
    - ``res/``: the program's resources (packed when building)
    - ``config/``: the tracker's configurations data, currently only hosting one example config file (not packed when building)
    - ``.github/``: hosts the GitHub workflows (to provide automated builds and releases)
    - ``.vscode/``: settings and launch profiles for Visual Studio Code

## Creating a configuration

To create your own configuration, start by creating a directory named ``config``. For executable builds you need to place it in the folder where the executable is located, if running from source it needs to be in the same folder where the ``src`` folder is (see how this repository does this)

Next, add a subfolder in the folder you just created, the name doesn't matter. Every file in this subfolder can be named and organised like you want, the only file that requires a fixed path and name is ``config.xml``, that should be located at the top-level of the config's subfolder (example: ``config/oot/config.xml``)

The content of the XML file need to follow some rules, you can look at the example config in this repo for now, the example configuration have some documentation about the layout of the file (I'm gonna be honest, I'm just too lazy to explain it properly there but that's on my TODO list)

The background image's width and height will be used to set the window's width and height.

Small notes on items:
- To create a progressive item (something that have a different texture when you get an upgrade (for example: the hookshot on OoT)) you just need to specify the path to the next upgrade's texture in the ``Sources`` (separated by a ``;``)

- To create an item that have different capacities (for example: the deku sticks on OoT), add ``Tiers="10;20;30"`` with the different tiers the item can have

- If the item doesn't have both it will be considered as a simple "on/off" item

- To set the item's position simple use ``Pos="X;Y"`` with ``X`` and ``Y`` being decimal values
