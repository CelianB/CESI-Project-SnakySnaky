#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import client

def on_input(event):
	print('On input')

def on_update():
	print('On update')

def on_render():
	print('On render')

win = client.Window('Cobra', 800, 600, 30)

win.run(input=on_input, update=on_update, render=on_render)