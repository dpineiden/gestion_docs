#archivo de parametros
awk -F';' -v Nbase="$Posicion_base" -v Nfilas="$N_filas" '(NR>Nbase && NR<=(Nbase+Nfilas)){print $2}' SSE_matriz_test.csv > DAT_MATRIX/parametros.dat
#archivo de contenedores
awk -F';' -v Nbase="$Posicion_base" -v Nfilas="$N_filas" -v Plab="$N_Lab" '(NR>Nbase && NR<=(Nbase+Nfilas)){print $(Plab+1)}' SSE_matriz_test.csv > DAT_MATRIX/pre_contenedores.dat
#archivo de estaciones
awk -F';' -v Nest="$Posicion_ME" -v Neq="$Posicion_EQMAT" -v Plab="$N_Lab" '(NR>Nest && NR<=(Neq-2)){print $1}' SSE_matriz_test.csv > DAT_MATRIX/estaciones.dat
cd DAT_MATRIX
cat pre_contenedores.dat | sort | uniq > contenedores.dat 
cd ..

