 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#Otro gestor de ODF
#https://pythonhosted.org/ezodf/variable_managment.html
from ezodf import opendoc
#Se abre appy pod
from appy.pod.renderer import Renderer
import xml.sax
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#Uso de regular expresions
import re
#Importar librerias para trabajar con csv
import csv
import os
import subprocess

#####################
###Librerias custom
sys.path.insert(0, '/home/david/Documents/AutomatizaciónFL/Oficial/py_libs/')
import py_libs                               
from py_libs import *             
from arraydict2string import arraydict2string
#####################

delimiter=';'
fieldnames_param=['parametro']
fieldnames_contenedor=['contenedor']
fieldnames_estacion=['estacion']
ruta_param="DAT_MATRIX/parametros.dat"
ruta_contenedores="DAT_MATRIX/contenedores.dat"
ruta_estaciones="DAT_MATRIX/estaciones.dat"
PARAM=[]
CONT=[]
EST=[]
with open(ruta_param) as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_param,delimiter)
  for row in reader:
   PARAM.append(row)
   
with open(ruta_contenedores) as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_contenedor,delimiter)
  for row in reader:
   CONT.append(row)
   
with open(ruta_estaciones) as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_estacion,delimiter)
  for row in reader:
   EST.append(row)
   
n_PARAM=len(PARAM)
n_CONT=len(CONT)
n_EST=len(EST)


Nombre_Proyecto=os.environ["Nombre_Proyecto"]
Codigo_Proyecto=re.sub(' ' ,'',os.environ["Codigo_Proyecto"])
Nombre_Area=os.environ["Nombre_Area"]
Nombre_Solicita=os.environ["Nombre_Solicita"]
Fecha_Solicita=os.environ["Fecha_Solicita"]
Fecha_Entrega=os.environ["Fecha_Entrega"]

key_est = 'estacion'
key_cont = 'contenedor'
key_param = 'parametro'
label_td = 'td'
label_tr = 'tr'
s_estacion = arraydict2string(EST,key_est,label_td)
s_contenedor = arraydict2string(CONT,key_cont,label_tr)
s_param = arraydict2string(PARAM,key_param,label_tr)

#Se genera el codigo html para la cantidad de estaciones
col_vacia="<td></td>"
empty_cols=col_vacia*n_EST
#se reemplaza el string </td> de cada param y contender, por </td>+empty_cols
s1_param = s_param.replace('<tr>','<tr><td>')
s2_param = s1_param.replace('</tr>','</td></tr>')

s1_contenedor = s_contenedor.replace('<tr>','<tr><td>')
s2_contenedor = s1_contenedor.replace('</tr>','</td></tr>')

s3_param = s2_param.replace('</td>','</td>'+empty_cols)
s3_contenedor = s2_contenedor.replace('</td>','</td>'+empty_cols)

html_estacion_param = "<table>" + "<tr><td>Parámetro\\Estación</td>" + s_estacion + "</tr>" + s3_param + "</table>"
html_estacion_contenedor = "<table>" + "<tr><td>Contenedor\\Estación</td>" + s_estacion + "</tr>" + s3_contenedor + "</table>"

print html_estacion_param 
print html_estacion_contenedor

Plantilla='templates/Matrices.ods'
Salida='salida/Matrices_'+Codigo_Proyecto+'_'+Fecha_Solicita+'.ods'

#Opccion APPY
renderer=Renderer(
  Plantilla,	#Plantilla
  globals(),	#Contexto
  Salida	#Salida
  )			

renderer.run()

#Opcion EZODF
spreadsheet = ezodf.newdoc(doctype="ods",filename=Plantilla)
#Crear dos tablas, una para estacion parametros, otra para contenedor.
Tabla_EP = Table("Parametros_Estaciones",size=(n_PARAM+1,n_EST+1),xml=None)
Tabla_EC = Table("Parametros_COntenedores",size=(n_PARAM+1,n_EST+1),zml=None)

