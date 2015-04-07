#!/bin/bash 
echo "Se ha ejecutado el scripts desde python!! Muy bien!"
pwd
path="./procesa_fl/sse_files/Patron_FL.xlsx"
destino="./procesa_fl/procesa_sse/."
echo "cp "$path" ."
cp $path $destino