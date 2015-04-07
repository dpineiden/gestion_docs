matriz=("agua dulce" "agua salobre" "sedimento")
elementos=$(echo ${#matriz[@]})
for ((i=1;i<=$elementos;i++))
do
this_matriz=${matriz[i-1]}
awk -v this_matriz="$this_matriz" -F';' 'BEGIN{printf this_matriz}(NR==1){for (i=1;i<NF;i++){if(toupper($i)~toupper(this_matriz)){printf ";"i}}}' SSE_matriz.csv | awk 'NC>1{print $0>>"columnas_matriz.csv"}' 
done


