#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appy.pod.renderer import Renderer

numeros = range(1,101)

renderer = Renderer(
    'ex_05.odt',
    locals(), 
    'out_05.odt',
    )
renderer.run()
