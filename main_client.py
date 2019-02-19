#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import client

win = client.Window('Cobra', 800, 600, 30)

game = client.Game(win)

win.run(input=game.on_input, update=game.on_update, render=game.on_render)