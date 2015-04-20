#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appy.pod.renderer import Renderer

flag = False

renderer = Renderer(
    'ex_04.odt',
    locals(), 
    'out_04.odt',
    )
renderer.run()
