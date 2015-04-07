#Se usan valores de:
BASE="PRE_CSV/SSE_matriz_test.csv"
#Obtener parametros
awk -v PBASE="$Posicion_base" -v PME="$Posicion_ME" -F';' '(FNR>PBASE && FNR <(PME-2)){print $2}' $BASE > parametros.dat
#Obtener COD_CONTENEDORES
awk -v PBASE="$Posicion_base" -v PME="$Posicion_ME" -F';' '(FNR>PBASE && FNR <(PME-2)){print $9}' $BASE > pre_contentedores.dat
sort -u pre_contentedores.dat | sed '/^$/d' > contenedores.dat
rm pre_contentedores.dat
#oBTENER LISTA DE ESTACIONES
awk -v PME="$Posicion_ME" -v PEQMAT="$Posicion_EQMAT" -F';' '(FNR>PME && FNR <PEQMAT){print $1}' $BASE > estaciones.dat

mv *.dat DAT_MATRIX
