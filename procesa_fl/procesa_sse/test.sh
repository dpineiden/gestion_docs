#!/bin/bash 
echo "Se ha ejecutado el scripts desde python!! Muy bien!"
pwd
path="../sse_files/Patron_FL.xlsx"
destino=" ."
echo "cp "$path$destino
cp $path $destino
pwd
./extrac_data_oficial.sh -f Patron_FL.xlsx