#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import client
from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')

#Initialisation de la fenetre
win = client.Window(config_general.getStr('Title'), config_general.getInt('ScreenWidth'), config_general.getInt('ScreenHeight'), 10)

game = client.Game(win)

win.run(input=game.on_input, update=game.on_update, render=game.on_render)