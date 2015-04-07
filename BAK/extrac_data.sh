#Pasar Planilla Matriz a CSV,se coloca el numero de la hoja matriz en planilla a convertir
hoja_matriz=2
#Comando que convierte hoja de una planilla en CSV
file_sse="SSE_matriz.csv"
xlsx2csv -d ';' -s$hoja_matriz SSE_b.xlsx $file_sse
#Se obtiene el nro de filas del archivo
N_filas=$(awk 'END{print NR}' $file_sse)
patron_eliminar=';;;;;;;;;;;;;;;;;;;;';
sed -i '/'$patron_eliminar'/d' SSE_CCE.csv 
#Obtener la fila en que parten los datos
#Extraer los datos
#Lista de laboratorios
Laboratorios=("CEA" "SGS" "ALS" "BIODIVERSA" "HIDROLAB")
Cant_lab=$(echo ${#Laboratorios[@]})
#Numero de Columna de laboratorios
N_Lab=$(awk -F';' '(FNR==1){for (i=1;i<=NF;i++){if($i~"Laboratorio"){print i}}}' $file_sse)
#Con N_filas y N_Lab se pueden obtener los datos de cantidades de muestras por estacion y su caracteristica de matriz fisica
#Paso los datos a un archivo que consulto con awk
#Se define un arra con los valore de filas y columna de laboratorio, esto da
#lo necesario para obtener la información para la obtencion de datos
#Esto es dado que la cantidad de columnas varia en función de la cantidad de estaciones
limites=($N_filas $N_Lab)
#Generar las listas de columnas asociadas con matriz fisica
matriz=("agua dulce" "agua salobre" "sedimento")
elementos=$(echo ${#matriz[@]})
for ((i=1;i<=$elementos;i++))
do
this_matriz=${matriz[i-1]}
awk -v this_matriz="$this_matriz" -F';' 'BEGIN{printf this_matriz}(NR==1){for (i=1;i<NF;i++){if(toupper($i)~toupper(this_matriz)){printf ";"i}}}' SSE_matriz.csv | awk 'NC>1{print $0>>"columnas_matriz.csv"}' 
done
#Reemplazar espacios por guines bajos
sed -i 's/ /_/g' columnas_matriz.csv
##Leer el archivo columnas_matriz.csv para obtener unicamente las matrices que se miden en este proyecto
this_matrices=($(awk -F';' '{print $1}' columnas_matriz.csv))
N_matrices=$(cat columnas_matriz.csv | wc -l)
#EJ:
#echo ${this_matrices[0]}
#agua_dulce
#Parentesis adicionales provocan la deficion de un arreglo

#Leer los dos archivos y definir las variables de filas y col Laboratorio
awk -F';'
'BEGIN{
END(NR==FNR){
N_Filas=$1;
N_Lab=$2;
next
}
{
  for (i=2;i<N_Lab;i++)
  {
    print N_Filas, N_Lab
  }
}
}' $file_sse