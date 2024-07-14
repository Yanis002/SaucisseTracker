# SaucisseTracker

Work in progress item tracker for randomizers. Aims to be customizable easily with a built-in editor and import/export capabilities.

## Requirements

- Python (3.10+)
- PyQt6

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
