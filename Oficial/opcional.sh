#!/bin/sh
#Tutorial getops:http://wiki.bash-hackers.org/howto/getopts_tutorial
# A POSIX variable
OPTIND=1      

nuevo_archivo=0
#iniciar nuestas variables:
ARCHIVO="Patron_FL.xlsx"

while getopts "vf:" opt; do
  case $opt in
    f)	output_file=$OPTARG
	nuevo_archivo=1
	;;
    v)  verbose=1
	;;
    esac
done

if [ $nuevo_archivo -eq 1 ]; then
 ARCHIVO=$output_file
fi

echo $ARCHIVO

#si verbose=1 generar las preguntas