#!/usr/bin/env python

from appy.pod.renderer import Renderer
import datetime

hora = datetime.datetime.now()
renderer = Renderer(
    'ex_01.odt',     # Plantilla
    {'hora':hora},   # Contexto
    'out_01.odt'    # Salida
    )
renderer.run()
