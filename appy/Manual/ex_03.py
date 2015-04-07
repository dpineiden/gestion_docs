#!/usr/bin/env python

from appy.pod.renderer import Renderer

class Mensajes:
    def __init__(self, msg):
        self.msg = msg

    def hola(self):
        return self.msg

mensajes = Mensajes('hola, mundo')

datos = [
    {'nombre':'Matt Murdock'},
    {'nombre':'Peter Parker'},
    ]

renderer = Renderer('ex_03.odt', globals(), 'out_03.odt')
renderer.run()
