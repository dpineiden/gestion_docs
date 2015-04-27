#PRimero extraer datos

#Luego generar el FL y R08 con python

#Convertir a documentos Microsoft
mv *.ods $OUT_FOLDER
mv *.odt $OUT_FOLDER
cd $OUT_FOLDER
mkdir ODF 
unoconv -f doc *.odt
unoconv -f xls *.ods
mv *.ods ODF/
mv *.odt ODF/
cd ..
zip -r $OUT_FOLDER".zip" $OUT_FOLDER