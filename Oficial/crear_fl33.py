#!/usr/bin/env python
# -*- coding: utf-8 -*-
from appy.pod.renderer import Renderer
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#Uso de regular expresions
import re
#Importar librerias para trabajar con csv
import csv
delimiter=';'
fieldnames_me=['matriz','estaciones']
fieldnames_fl33=['lab','matriz','n_estaciones','parametro','replicas']
fieldnames_r08=['lab','matriz','n_estaciones','parametro','replicas','n_cotizacion','costo','unidad_costo']
fieldnames_obs=['lab','matriz','observacion']
fieldnames_equ=['equipo','cantidad']
fieldnames_adj=['lab','matriz','info']
fieldnames_lab=['lab','direccion','horario','telefono','contacto']
###Importar variables desde bash
#import subprocess
import os
import subprocess
#subprocess.call("source k.sh",shell=True)
#Generador: grep "export" extrac_data_oficial.sh | awk -F'=' '{print $1}' | awk '{print  $2"=os.environ[\""$2"\"]"}'
Excel=os.environ["Excel"]
file_sse=os.environ["file_sse"]
Nombre_Proyecto=os.environ["Nombre_Proyecto"]
Codigo_Proyecto=re.sub(' ' ,'',os.environ["Codigo_Proyecto"])
Nombre_Area=os.environ["Nombre_Area"]
Nombre_Solicita=os.environ["Nombre_Solicita"]
Fecha_Solicita=os.environ["Fecha_Solicita"]
Fecha_Entrega=os.environ["Fecha_Entrega"]
Posicion_base=os.environ["Posicion_base"]
Posicion_ME=os.environ["Posicion_ME"]
N_filas=os.environ["N_filas"]
#array:
Laboratorios=os.environ["str_laboratorios"]
Cant_lab=os.environ["Cant_lab"]
N_Lab=os.environ["N_Lab"]
#array:
str_limites=os.environ["str_limites"]
#array:
str_matriz=os.environ["str_matriz"]
this_matriz_estaciones=os.environ["this_matriz_estaciones"]
this_matrices=os.environ["str_this_matrices"]
N_matrices=os.environ["N_matrices"]
##
Plantilla='templates/FL33.odt'
Plantilla_R08='templates/R08.ods'
Salida='salida/FL33_'+Codigo_Proyecto+'_'+Fecha_Solicita+'.odt'

Proyecto = {
  'nombre':Nombre_Proyecto,
  'codigo':Codigo_Proyecto,
  'persona':Nombre_Solicita,
  'area':Nombre_Area,
  'fecha_solicita':Fecha_Solicita,
  'fecha_entrega':Fecha_Entrega}

ME = []
CEASA = []
R08 = []
OBS=[]
EQU=[]
ADJ=[]
LAB=[]
#Ahora, se deben leer los archivos csv:
#matriz_estaciones.csv contiene la relacion de matriz con la lista de matriz_estaciones
with open('PRE_CSV/matriz_estaciones.csv') as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_me,delimiter=':')
  for row in reader:
    ME.append(row)
    
#CEASA_FL33.csv contiene los datos de matrices y parametros que van a CEASA, se llena con esto el FL33
with open('PRE_CSV/CEASA_FL33.csv') as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_fl33,delimiter=delimiter)
  for row in reader:
    CEASA.append(row)   
    
#CEASA_FL33.csv contiene los datos de matrices y parametros que van a CEASA, se llena con esto el FL33
with open('PRE_CSV/observaciones.csv') as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_obs,delimiter=delimiter)
  for row in reader:
    OBS.append(row) 

#CEASA_FL33.csv contiene los datos de matrices y parametros que van a CEASA, se llena con esto el FL33
with open('PRE_CSV/equipos_cea.csv') as csvfile:
  reader=csv.DictReader(csvfile,fieldnames_equ,delimiter=delimiter)
  for row in reader:
    EQU.append(row)     
    
#OrdenCOmpra.csv contiene los datos de los laboratorios en que hay que hacer ordenes de compra
with open('PRE_CSV/OrdenCompra.csv') as csvfile: 
  reader=csv.DictReader(csvfile,fieldnames_r08,delimiter=delimiter)
  for row in reader:
    R08.append(row)

#adjuntos.csv contiene afirmacion o negacion de si hay documentos adjuntos
with open('PRE_CSV/adjuntos.csv') as csvfile: 
  reader=csv.DictReader(csvfile,fieldnames_adj,delimiter=delimiter)
  for row in reader:
    ADJ.append(row)    

#SSE_labs.csv contiene los datos de los laboratorios
with open('PRE_CSV/SSE_labs.csv') as csvfile: 
  reader=csv.DictReader(csvfile,fieldnames_lab,delimiter=delimiter)
  for row in reader:
    LAB.append(row) 

##################
#Generar arreglo de datos para llenado de plantilla
#cantidad de datos por listado
n_me=len(ME)
n_ceasa=len(CEASA)
#Se inicializa variable de input a plantilla
Data=[]
#Llenar los campos de las distintas matrices
Existe_Grupo=False
for i in range(0,n_ceasa):
  matriz=CEASA[i]['matriz']
  item_matriz={'matriz':matriz}  
  LD=len(Data)  
  if LD==0:
   Data.append(item_matriz)     
  LD=len(Data)  
  for j in range(0,LD):
   Existe_Grupo = (matriz in Data[j].values())   
  if not Existe_Grupo:
   Data.append(item_matriz)   

  #se agrega item al mismo diccionario
   
###
N_Grupos=len(Data)
n_datos=[]
#Inicializar campo dato en cada Posicion
for i in range(0,N_Grupos):
  Data[i]['datos']=[]
#para cada matriz llenar el campo dato con un diccionario de valores  
for i in range(0,N_Grupos):
  matriz=Data[i]['matriz']
  for j in range(0,n_ceasa):
   matriz_ceasa=CEASA[j]['matriz'] 
   if (matriz_ceasa == matriz):
     #Añadir la lista de datos asociada a matriz
     llaves=CEASA[j].keys() 
     ll_m=llaves.index('matriz')
     datos={k : CEASA[j][k] for k in llaves[:ll_m]}
     Data[i]['datos'].append(datos) 
##Añadir estaciones a cada matriz
  for j in range(0,n_me):
   matriz_me=re.sub('_' ,' ',ME[j]['matriz']) 
   if (matriz_me == matriz):
     #Añadir la lista de datos asociada a matriz
     llaves=ME[j].keys() 
     ll_m=llaves.index('matriz')
     estaciones={k : ME[j][k] for k in llaves[:ll_m]}
     Data[i]['estaciones']=estaciones['estaciones']
     Data[i]['observaciones']='' 
     

###Leer Orden de Compra y crear R08     
Data_R08=[]
n_r08=len(R08)
Existe_Grupo = True
for i in range(0,n_r08):
  lab=R08[i]['lab']
  item_lab={'lab':lab}
  LD=len(Data_R08)  
  if LD==0:
   Data_R08.append(item_lab)
  LD=len(Data_R08)
  j=0
  while (Existe_Grupo and j<LD):
   Existe_Grupo = (lab in Data_R08[j].values()) 
   j=1+j
  if not Existe_Grupo:
   Data_R08.append(item_lab)    

#Agregar datos de los parametros a medir correspondientes a cada LAB para el R08   
###
N_Grupos_R08=len(Data_R08)
n_datos_R08=[]
#Inicializar campo dato en cada Posicion
for i in range(0,N_Grupos_R08):
  Data_R08[i]['datos']=[]
#para cada matriz llenar el campo dato con un diccionario de valores  
for i in range(0,N_Grupos_R08):
  matriz=Data_R08[i]['lab']
  for j in range(0,n_r08):
   matriz_R08=R08[j]['lab'] 
   if (matriz_R08 == matriz):
     #Añadir la lista de datos asociada a matriz
     llaves=R08[j].keys()
     ll_m=llaves.index('lab')
     ac=llaves.pop(ll_m)
     datos={k : R08[j][k] for k in llaves}
     Data_R08[i]['datos'].append(datos) 
  
     
#Añadir las observaciones asociadas a cada matriz
n_obs=len(OBS)

OBS_R08=[]
for i in range(0,N_Grupos):
  matriz=Data[i]['matriz']
  for j in range(0,n_obs):
   lab=OBS[j]['lab']
   matriz_obs=OBS[j]['matriz']
   pre_obs=OBS[j]['observacion']   
   observacion='<p>'+re.sub('\\\\n','</p><p>',pre_obs)+'</p>'
   if (lab == 'CEA' and matriz_obs == matriz ):
     Data[i]['observaciones']=observacion
   if (lab != 'CEA'):
     OBS_R08.append({'lab':lab,'observacion':observacion})
#Pasar OBS_R08 a Data_R08
n_obs_r08=len(OBS_R08)
for i in range(0,N_Grupos):
  lab_r08=Data_R08[i]['lab']
  #Agregar observacion vacia a cada posicion de laboratorios
  Data_R08[i]['observaciones']=''
  for j in range(0,n_obs_r08):      
   lab_obs=OBS_R08[j]['lab']
   if ( lab_r08 == lab_obs ):
    observacion=OBS_R08[j]['observacion']
    Data_R08[i]['observaciones']=observacion
    
    
##Pasar info de si adjunta o no documentos
#ADJ
n_adj= len(ADJ)
for i in range(0,N_Grupos_R08):
  lab_r08=Data_R08[i]['lab']
  #Agregar observacion vacia a cada posicion de laboratorios
  Data_R08[i]['adjunta']=''
  for j in range(0,n_adj):      
   lab_adj=ADJ[j]['lab']
   if ( lab_r08 == lab_adj ):
    info=ADJ[j]['info']
    if ( info == "si" ):
     Data_R08[i]['adjunta']=info   


##Pasar información de contacto de lanboratorio
cant_labs=len(LAB)
for i in range(0,N_Grupos_R08):
  lab_r08=Data_R08[i]['lab']
  #Agregar observacion vacia a cada posicion de laboratorios
  Data_R08[i]['datos_lab']=''
  for j in range(0,cant_labs):      
   lab=LAB[j]['lab']
   if ( lab_r08 == lab ):
    direccion=re.sub('\\\\n','\n',LAB[j]['direccion'])+'-\n'
    telefono=re.sub('\\\\n','\n',LAB[j]['telefono'])+'-\n'
    contacto=re.sub('\\\\n','\n',LAB[j]['contacto'])+'\n'
    Data_R08[i]['datos_lab']=direccion+telefono+contacto 

#Añadir los instrumentos a solicitiar e FL33
#tiene una estructura similar a Data[i]['datos'] como un arreglo de diccionarios
#Se debe añadir directamente la lista a Data['equipos'][*]
##['equipo','cantidad']
# equipo=EQU[i]['equipo']
# cantidad=EQU[i]['cantidad']
n_equ = len(EQU)
g_equip=range(0,n_equ)
     
#generar los rangos de datos para cada matriz
for i in range(0,N_Grupos):
  n_datos.append(len(Data[i]['datos']))
####intervalos de iteracion
grupos=range(0,N_Grupos)
int_n_datos=[]
for i in range(0,len(n_datos)):
  int_n_datos.append(range(0,n_datos[i]))

#generar los rangos de datos para cada matriz de R08
for i in range(0,N_Grupos_R08):
  n_datos_R08.append(len(Data_R08[i]['datos']))


LAb_Data_R08=[]
N_labs=len(Data_R08)

####intervalos de iteracion
grupos_r08=range(0,N_Grupos_R08)
int_n_datos_r08=[]
for i in range(0,len(n_datos_R08)):
  int_n_datos_r08.append(range(0,n_datos_R08[i]))
  
############Llenar plantilla
renderer=Renderer(
  Plantilla,	#Plantilla
  globals(),	#Contexto
  Salida	#Salida
  )			

renderer.run()

#Crear los R08
#POr cada lab
#Ajustar nueva variable ---> LAB
#Cargar datos en plantilla y guardar en nuevo archivo
LAB_Data_R08=[]
N_labs=len(Data_R08)

for i in range(0,N_labs):
 len(Data_R08[i]['datos']) 
 if len(Data_R08[i]['datos'])>0 :
  LAB_Data_R08={'lab':Data_R08[i]['lab'],'adjunta':Data_R08[i]['adjunta'],'datos':Data_R08[i]['datos'],'datos_lab':Data_R08[i]['datos_lab']}
  N_datos=int_n_datos_r08[i]
  #SE crea variable LAB_Data_R08['datos'][j]['*'] para cargar particularmente cada archivo
  Salida_R08='salida/R08_'+LAB_Data_R08['lab']+'_'+Codigo_Proyecto+'_'+Fecha_Solicita+'.ods'
  renderer_R08=Renderer(
    Plantilla_R08,	#Plantilla
    globals(),	#Contexto
    Salida_R08	#Salida
    )	
  renderer_R08.run()
  #Por cad alab hacer un archivo
#Salida_R08='salida/R08_'+Codigo_Proyecto+'_'+Fecha_Solicita+'.odt'