#!/usr/bin/env python

from appy.pod.renderer import Renderer
import datetime

hora = datetime.datetime.now()
def to_upper(s):
    return s.upper()
renderer = Renderer(
    'ex_02.odt', 
    globals(), 
    'out_02.odt'
    )
renderer.run()
