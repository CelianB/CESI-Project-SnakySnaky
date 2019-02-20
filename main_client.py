#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Florian Hervieux

from client import Window, Game
from client.events import EventBus
from util.config_mgmt import ConfigHandler

# Load config file
config_general = ConfigHandler('configs', False, 'config.ini', '')

# Inin event bus
event_bus = EventBus()

# Init window
win = Window(config_general.getStr('Title'), config_general.getInt('ScreenWidth'), config_general.getInt('ScreenHeight'), 10, event_bus=event_bus)

# Create game
game = Game(win, event_bus)

# Run game
win.run(input=game.on_input, update=game.on_update, render=game.on_render)