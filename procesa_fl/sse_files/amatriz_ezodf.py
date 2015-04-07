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

##Importar variables de proyecto
No_solicitud=os.environ["No_solicitud"]
Nombre_Proyecto=os.environ["Nombre_Proyecto"]
Codigo_Proyecto=re.sub(' ' ,'',os.environ["Codigo_Proyecto"])
Nombre_Area=os.environ["Nombre_Area"]
Nombre_Solicita=os.environ["Nombre_Solicita"]
Fecha_Solicita=os.environ["Fecha_Solicita"]
Fecha_Entrega=os.environ["Fecha_Entrega"]

###
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

#Para contenedor-estacion
Plantilla_CE='templates/R115.ods'
#Para parametros-estaciones
Plantilla_PE='templates/Param_Est.ods'

Salida_CE='salida/R115_'+Codigo_Proyecto+'_No_SSE_'+No_solicitud+'.ods'
Salida_PE='salida/Matriz_PE_'+Codigo_Proyecto+'_No_SSE_'+No_solicitud+'.ods'


#Generar R115 de contenedores estaciones
#Opcion EZODF: Se guarda la plantilla con el nombre del doc
Matriz_CE = newdoc(doctype="ods",filename=Salida_CE,template=Plantilla_CE)
#Cargar la hoja template en el python
Tabla_EC = Matriz_CE.sheets[0]
#En C6 es el código del proyecto
Tabla_EC['B6'].set_value(Codigo_Proyecto)
#Crear dos tablas, una para estacion parametros, otra para contenedor.

#Fila de llenado
row_matrix=11

n_cols=Tabla_EC.ncols()
n_rows=Tabla_EC.nrows()
count_cols=n_EST-n_cols+1
count_rows=n_rows+n_CONT-row_matrix

Tabla_EC.append_columns(count=count_cols)
Tabla_EC.append_rows(count=count_rows)

for i in range(1,n_EST):
  Tabla_EC[row_matrix-1,i].set_value(EST[i-1]['estacion'])

fila_end=row_matrix+n_CONT
for j in range(row_matrix,fila_end):  
  contenedor=CONT[j-row_matrix]['contenedor']
  Tabla_EC[j,0].set_value(contenedor)

#Se guarda la Matriz_CE como planilla ods

Matriz_CE.save()


###Parametros estaciones

Matriz_PE = newdoc(doctype="ods",filename=Salida_PE,template=Plantilla_PE)

Tabla_EP=Matriz_PE.sheets[0]

Tabla_EP['B4'].set_value(Codigo_Proyecto)
Tabla_EP['B5'].set_value(Nombre_Solicita)

row_matrix=11

n_cols=Tabla_EP.ncols()
n_rows=Tabla_EP.nrows()
count_cols=n_EST-n_cols+1
count_rows=n_rows+n_CONT-row_matrix

Tabla_EP.append_columns(count=count_cols)
Tabla_EP.append_rows(count=count_rows)


for i in range(1,n_EST):
  Tabla_EP[row_matrix-1,i].set_value(EST[i-1]['estacion'])

fila_end=row_matrix+n_CONT
for j in range(row_matrix,fila_end):
  parametro=PARAM[j-row_matrix]['parametro']
  Tabla_EP[j,0].set_value(parametro)

Matriz_PE.save()

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