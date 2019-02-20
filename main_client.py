#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from client import Window, Game
from client.events import EventBus
from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')

event_bus = EventBus()

win = Window(config_general.getStr('Title'), config_general.getInt('ScreenWidth'), config_general.getInt('ScreenHeight'), 10, event_bus=event_bus)

game = Game(win, event_bus)

win.run(input=game.on_input, update=game.on_update, render=game.on_render)