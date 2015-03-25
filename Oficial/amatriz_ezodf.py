 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#Otro gestor de ODF
#https://pythonhosted.org/ezodf/variable_managment.html
from ezodf import opendoc
#Se abre appy pod
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
from ezodf import newdoc, Paragraph, Heading, Sheet, opendoc, Cell

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

Plantilla='templates/Matrices.ods'
Salida='salida/Matrices_'+Codigo_Proyecto+'_'+Fecha_Solicita+'.ods'

#Opcion EZODF
Matrices = newdoc(doctype="ods",filename=Salida)
#Se añaden las dos hojas del spreadsheet

#Crear dos tablas, una para estacion parametros, otra para contenedor.
sheets= Matrices.sheets

Tabla_EP = Sheet("Parametros_Estaciones",size=(n_PARAM+1,n_EST+1))
Tabla_EC = Sheet("Contenedores_Estaciones",size=(n_PARAM+1,n_EST+1))

sheets += Tabla_EP
sheets += Tabla_EC
Estilo_TABLA="""<style:style style:name="estilo_tabla" style:family="table" style:master-page-name="Default">
<style:table-properties table:display="true" style:writing-mode="lr-tb"/>
</style:style>"""
Estilo_COLUMNA="""<style:style style:name="co3" style:family="table-column">
<style:table-column-properties fo:break-before="auto" style:column-width="4.5cm"/>
</style:style>"""
Estilo_CELDA_PAR="""<style:style style:name="ce1" style:family="table-cell" style:parent-style-name="Default">
<style:table-cell-properties fo:border="0.06pt solid #000000"/>
<style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
</style:style>"""
Estilo_CELDA_CON="""<style:style style:name="ce2" style:family="table-cell" style:parent-style-name="Default">
<style:table-cell-properties fo:border="0.06pt solid #000000"/>
<style:text-properties fo:color="#660033" fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
</style:style>
<style:style style:name="ce3" style:family="table-cell" style:parent-style-name="Default">
<style:table-cell-properties fo:border="0.06pt solid #000000"/>
<style:text-properties fo:color="#006633" fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
</style:style>"""

Matrices.inject_style(Estilo_TABLA+Estilo_COLUMNA+Estilo_CELDA_PAR+Estilo_CELDA_CON)

Tabla_EP.style_name="estilo_tabla"
Tabla_EC.style_name="estilo_tabla"

Tabla_EP['A1'].set_value('Parámetro\\Estación')
Tabla_EP['A1'].style_name="ce1"
Tabla_EC['A1'].set_value('Contenedor\\Estación')
Tabla_EC['A1'].style_name="ce1"


for i in range(1,n_EST):
  Tabla_EP[0,i].set_value(EST[i-1]['estacion'])
  Tabla_EC[0,i].set_value(EST[i-1]['estacion'])

for j in range(1,n_PARAM):
  Tabla_EP[j,0].set_value(PARAM[j-1]['parametro'])

for j in range(1,n_CONT)  :
  Tabla_EC[j,0].set_value(CONT[j-1]['contenedor'])

index = sheets.names()

Matrices.save()
#----EJEMPLO: https://pypi.python.org/pypi/ezodf
#ods = newdoc(doctype='ods', filename='spreadsheet.ods')
#sheet = Sheet('SHEET', size=(10, 10))
#ods.sheets += sheet
#sheet['A1'].set_value("cell with text")
#sheet['B2'].set_value(3.141592)
#sheet['C3'].set_value(100, currency='USD')
#sheet['D4'].formula = "of:=SUM([.B2];[.C3])"
#pi = sheet[1, 1].value
#ods.save()