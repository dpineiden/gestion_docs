#!/bin/bash
#Tutorial getops:http://wiki.bash-hackers.org/howto/getopts_tutorial
# A POSIX variable
OPTIND=1      

verbose=1
nuevo_archivo=0
#iniciar nuestas variables:
ARCHIVO="Patron_FL.xlsx"

while getopts "vf:" opt; do
  case $opt in
    f)	output_file=$OPTARG
	nuevo_archivo=1
	verbose=0
	;;
    v)  verbose=1
	;;
    esac
done

if [ $nuevo_archivo -eq 1 ]; then
 ARCHIVO=$output_file
fi

cp "../sse_files/"$ARCHIVO .
. extrac_data_oficial.sh -f $ARCHIVO
python crear_fl33.py 
python amatriz_ezodf.py 
cd salida/
./proceso.sh 
cd ..
mv $ARCHIVO R114/
 
