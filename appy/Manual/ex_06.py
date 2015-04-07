#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appy.pod.renderer import Renderer
ejemplo = '''
<h2>Ejemplo</h2>
<p>Un párrafo con <b>negritas</b>, <i>itálicas</i>, subíndices:
H<sub>2</sub>O, exponentes:  2·π·r<sup>2</sup> y de postre un enlace:
<a href="http://www.python.org/">www.python.org</a>.</p>
<ul>
    <li>Uno</li>
    <li>Dos</li>
    <li>Tres</li>
      <ul>
      <li>Tres.Uno</li>
      <li>Tres.Dos</li>
      </ul>
</ul>
'''
renderer = Renderer('ex_06.odt', locals(), 'out_06.odt',)
renderer.run()
