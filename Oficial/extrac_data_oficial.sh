#!/bin/bash
#Borrar valores de variables anteriores
unset Excel
unset file_sse
unset Nombre_Proyecto
unset Codigo_Proyecto
unset Nombre_Solicita
unset Fecha_Solicita
unset Fecha_Entrega
unset Posicion_base
unset Posicion_ME
unset Posicion_OBS
unset N_filas
unset Cant_lab
unset N_Lab
unset this_matriz_estaciones
unset N_matrices
unset arrays
unset str_laboratorios
unset str_limites
unset str_matriz
unset str_this_matrices
#Pasar Planilla Matriz a CSV,se coloca el numero de la hoja matriz en planilla a convertir
hoja_matriz=1
hoja_labs=2
#Nombre de archivo excel
read -t 10 Excel
if [ "${#Excel}" -eq "0" ]; then
 Excel="Patron_FL.xlsx"
fi
export Excel
#Nombre archivo CSV
export file_sse="SSE_matriz_test.csv"
export file_labs="SSE_labs.csv"
#Comando que convierte hoja de una planilla en CSV, -d es delimitador, -s indica la hoja, -e indica que reemplaza caracteres de escape
xlsx2csv -d ';' -s$hoja_matriz -e $Excel $file_sse 
xlsx2csv -d ';' -s$hoja_labs -e $Excel $file_labs 
#Borrar encabezado de lista de laboratorios
sed -i '1d' $file_labs
#Extraer nombre de proyecto
export Nombre_Proyecto=$(grep "Nombre Proyecto" $file_sse | awk -F';' '{print $2}')
#Extraer area que solicita
export Nombre_Area=$(grep "Área Solicita" $file_sse | awk -F';' '{print $2}')
#Extraer codigo proyecto
export Codigo_Proyecto=$(grep "Código Proyecto" $file_sse | awk -F';' '{print $2}')
#Extraer persona que solicita
export Nombre_Solicita=$(grep "Solicitado por" $file_sse | awk -F';' '{print $2}')
#Extraer fecha solicitud
export Fecha_Solicita=$(grep "Fecha Solicitud" $file_sse | awk -F';' '{print $2}'|sed 's/\//-/g')
#Extraer fecha entrega
export Fecha_Entrega=$(grep "Fecha Entrega de Material" $file_sse | awk -F';' '{print $2}'|sed 's/\//-/g')
#si se trabaja con 'date' sera necesario pasar la primera cifra a segundo lugar y la segunda a primer lugar
export Posicion_base=$(grep -nr 'Cantidad (N° estaciones)' $file_sse | awk -F':' '{print $1}')
#Donde esta la matriz de estiaciones/matriz fisica? obtener la posicion de linea
export Posicion_ME=$(grep -nr 'Matriz\\Estaciones' $file_sse | awk -F':' '{print $1}')
#Obtener posicion instrumentos
export Posicion_EQMAT=$(grep -nr 'Equipos-Materiales' $file_sse | awk -F':' '{print $1}')
#Obtener posicion obsevaciones
export Posicion_OBS=$(grep -nr 'Observaciones\\Lab' $file_sse | awk -F':' '{print $1}')
#Obtener posicion adjunta
export Posicion_ADJ=$(grep -nr 'ADJUNTA' $file_sse | awk -F':' '{print $1}')
#Obtener numero de filas de matriz base
export N_filas=$((($Posicion_ME-1)-($Posicion_base)))
#Obtener la fila en que parten los datos
#Extraer los datos
#Lista de laboratorios
Laboratorios=("CEA" "SGS" "ALS" "BIODIVERSA" "HIDROLAB" "AGUAS INDUSTRIALES LTDA")
export Cant_lab=$(echo ${#Laboratorios[@]})
#Numero de Columna de laboratorios
export N_Lab=$(awk -F';' -v Posicion="$Posicion_base" '{
if (FNR==Posicion)
{
for (i=1;i<=NF;i++)
{
if($i~"Laboratorio")
{
print i;
}
}
}
}' $file_sse)
#Arreglo de limites de bloque 2 y numero de filas
limites=($Posicion_base $N_filas $N_Lab)
#Generar las listas de columnas asociadas con matriz fisica
#si se añade otra matriz agregar abajo en pre_matriz tb
matriz=(
"Agua Marina"
"Agua Salar"
"Agua Salar Dulce"
"Agua Dulce"
"Sedimento Marino"
"Sedimento Salar"
"Sedimento Salar Dulce"
"Sedimento Dulce"
)
export elementos=${#matriz[@]}
#Obtener los nombres de las estaciones en un arreglo al leer las filas desde Posicion_ME+1 hasta fila -1 de Equipos-Materiales, 
#a partir de la segunda columna hasta NF(numero de campos)
#Busco en el tercer bloque, a partr de Posicion_ME+1, en los campos a partir de 2. Si tiene valor 1, entonces registrar la relacion de estacion con matriz 
for ((i=0;i<=$elementos-1;i++))
do
this_matriz=${matriz[i]} 
awk -v this_matriz="$this_matriz" -v Posicion="$Posicion_ME" -v EQMAT="$Posicion_EQMAT" -F';' 'BEGIN{x=1;}
{
if (FNR>=Posicion && FNR<EQMAT) 
{
  if(NR==Posicion) 
  {
    for (p=2;p<=NF;p++) 
    {
    if(length($p) > 0) 
    {
      Matriz[p-1]=$p; 
    }
  }
  };
  Cantidad_Matrices=length(Matriz);
  if(NR>Posicion) 
  {
  k=1;
  for (p=2;p<=Cantidad_Matrices+1;p++){
      if (toupper(Matriz[p-1])~toupper(this_matriz) && $p==1){
	  this_estacion[k]=$1;
	  k=k+1;      
    }
  };
  if(k>1)
	{
	if (x==1){
	printf this_matriz;
	x=0;
	}
	for (m=1;m<=length(this_estacion);m++)
	  {
		printf ";"this_estacion[m];
	  }
	}
      }
  }
}' $file_sse| awk '{print>>"matriz_estaciones.csv"}';
done
##
#Reemplazar espacios por guines 
export this_matriz_estaciones="matriz_estaciones.csv"
#Reemplazar espacios por guines bajos
sed -i 's/ /_/g' $this_matriz_estaciones
##Leer el archivo columnas_matriz.csv para obtener unicamente las matrices que se miden en este proyecto
this_matrices=($(awk -F';' '{print $1}' $this_matriz_estaciones))
export N_matrices=$(cat $this_matriz_estaciones | wc -l)
#EJ:
#echo ${this_matrices[0]}
#agua_dulce
#Parentesis adicionales provocan la deficion de un arreglo
for ((i=0;i<=$Cant_lab-1;i++))
  do
  # <nombre_laboratorio> es la variable que se ingresa para buscar segun la columna N_Lab
    Nombre_lab=${Laboratorios[i]}
    for ((j=0;j<=$N_matrices-1;j++))
      do
      #SI Laboratorio es CEA-->generar resumen-->FL33
      #Se genera un archivo con nombre <laboratorio>.csv
      #Con estructura:
      # matriz - cantidad - total_parametro - replicas por estacion
      #Para esto se capturan las variables de <nombre lab> <matriz-cols> y se usan los valores de Nfilas y NColLab
      #Un array de bash se puede ingresar en awk de la siguiente manera:
      # awk -v var="${test[*]}" '{n=split(var,test," ");print test[2]}' SSE_matriz.csv
      # <matriz-cols> es el arreglo que se ingresa para buscar solamente las columnas que corresponden a esa matriz
      #Entrega un string con el nombre y los indices:
      matriz_cols=$(grep ${this_matrices[j]} $this_matriz_estaciones | sed 's/_/ /g' )
      #dentro del awk:
      #  Separo el nombre de matriz de cols y obtengo los indices de las columnas, itero en la cantidad de ellas
      # las sumo, saco un promedio y obtengo el floor entero  del promedio 'replica=int(a/b)'
      #limites=($Posicion_base $N_filas $N_Lab)
      #Cada nueva variable en awk se debe ingresar antecediendo -v
      #awk -v var="${test[*]}" -v group="$Grupo" '{n=split(var,test," ");print test[2], group}' SSE_matriz.csv
      awk -F';' -v limit="${limites[*]}" -v matriz_cols="$matriz_cols" -v lab="$Nombre_lab" '{
      OFS=";";
      ncols=split(matriz_cols,columnas,";");
      nlim=split(limit,limites," ");
      Posicion=limites[1];
      N_filas=limites[2];
      N_Lab=limites[3];
      posicion_Matriz=N_Lab-3;
      posicion_Cotizacion=N_Lab+3;
      posicion_Costo=N_Lab+4;
      posicion_Unidad=N_Lab+5;
      if($N_Lab~lab && $posicion_Matriz ~ columnas[1] )
	{
	estaciones=$1;
	parametro=$2;
	replica=$3;
	N_cotizacion=$posicion_Cotizacion;
	Costo=$posicion_Costo;
	Unidad_Costo=$posicion_Unidad;
	if($N_Lab~"CEA")
	{
	  print lab,columnas[1], estaciones, parametro , replica >>"CEASA_FL33.csv";
	} 
	else if($N_Lab !~"CEA")
	{
	  print lab,columnas[1], estaciones, parametro , replica, N_cotizacion,Costo,Unidad_Costo>>"OrdenCompra.csv";
	}
	}
      }' $file_sse
      #Si laboratorio es de los otros--->Generar resumen-->R08
    done
  done

##Generar archivo de instrumentos para FL33
export Equipos="equipos_cea.csv"
#desde Posicion_EQMAT+1 hasta Posicion_OBS
awk -F';' -v EQMAT="$Posicion_EQMAT" -v OBS="$Posicion_OBS"  '{OFS=";";if (FNR>(EQMAT+1) && FNR<OBS){print $2,$1}}' $file_sse > $Equipos
##Generar archivos de Observaciones:
#Se ordena segun lab:matriz:comentario
for ((i=0;i<=$Cant_lab-1;i++))
  do
  # <nombre_laboratorio> es la variable que se ingresa para buscar segun la columna N_Lab
    Nombre_lab=${Laboratorios[i]}
    for ((j=0;j<=$N_matrices-1;j++))
      do
      # laboratorio-matriz - comentario
      #Para esto se capturan las variables de <nombre lab> <matriz-cols> y se usan los valores de Nfilas y NColLab
     #Entrega un string con el nombre y los indices:
      matriz_cols=$(grep ${this_matrices[j]} $this_matriz_estaciones |awk -F':' '{print $1}' |sed 's/_/ /g' )
      #dentro del awk:
      #  Separo el nombre de matriz de cols y obtengo los indices de las columnas, itero en la cantidad de ellas
      # las sumo, saco un promedio y obtengo el floor entero  del promedio 'replica=int(a/b)'
      #limites=($Posicion_base $N_filas $N_Lab)
      #Cada nueva variable en awk se debe ingresar antecediendo -v
            #&& $1~columnas[1]
      k=0      
      #awk -v var="${test[*]}" -v group="$Grupo" '{n=split(var,test," ");print test[2], group}' SSE_matriz.csv
      awk -F';' -v OBS="$Posicion_OBS" -v ADJ="$Posicion_ADJ" -v matriz_cols="$matriz_cols" -v lab="$Nombre_lab" -v nLab="$i" '(FNR>OBS){
      if (FNR<ADJ){
      OFS=";";
      ncols=split(matriz_cols,columnas,";");
      pos=int(nLab+2);
      if(length($pos)>0 && columnas[1]~$1) {
      print lab,$1,$pos >> "observaciones.csv";
      }
      if(length($pos)==0 && columnas[1]~$1) {
      print lab,$1,"No" >> "observaciones.csv";
      }
      }
      if (FNR==ADJ){
      if (length($pos)==0) $pos="no";
      print lab,$pos >> "double_adjuntos.csv";
      k=1;
      }      
      }' $file_sse 
      #Si laboratorio es de los otros--->Generar resumen-->R08
    done
  done
#Elimar repetidas en double_adjuntos

cat double_adjuntos.csv | sort | uniq > adjuntos.csv

####
sed -i 's/;/:/' $this_matriz_estaciones  
  #Exporta variables
  #Pasar arrays a strings y exportar
export str_laboratorios=$(echo ${Laboratorios[*]})
export str_limites=$(echo ${limites[*]})
#Pasar nombres de espacio a 
pre_matriz=(
"Agua_Marina"
"Agua_Salar"
"Agua_Salar_Dulce"
"Agua_Dulce"
"Sedimento_Marino"
"Sedimento_Salar"
"Sedimento_Salar_Dulce"
"Sedimento_Dulce"
)
export str_matriz=$(echo ${pre_matriz[*]})
export str_this_matrices=$(echo {this_matrices[*]})
##MOVER ARCHIVOS CREADOS A PRE_CSV

######################################
grep "export" extrac_data_oficial.sh | awk -F'=' '{print $1}' | awk '{print  $2"=os.environ[\""$2"\"]"}'|awk -F'=' '{exportar = "export " $1;exportar | getline d; close(exportar); print exportar}'>exporta_variables.sh

mv *.csv PRE_CSV