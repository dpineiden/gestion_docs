 #!/usr/bin/perl
 
use warnings;
use strict;
use Scalar::Util qw(reftype);
use OpenOffice::OODoc;
use Scalar::Util::Numeric qw(isint);
#File input: perl add_wors.pk < file.odt

my @file_input = split /\./,$ARGV[0];
print "Nombre :". $file_input[0]."\n";

#nombre sin extensión
my $file=$file_input[0];

#Nombres de archivo odt y pdf
my $in_file =$file.'.odt';
my $in_pdf_file =$file.'.pdf';

#Se abre archivo para su lectura
my $documenta = odfDocument(file => $in_file);
# Referencia oficial: http://search.cpan.org/dist/OpenOffice-OODoc/OODoc/Text.pod#appendTableRow%28table%29
#Buscar el total de veces que aparece XXNULLXX
#De esto para cada XXNULLXX en particular agregar ROW a la TABLA
#Bajo la condicion de que no aumente la cantidad de páginas
#Obtener el id de la tabla en que esta un caracter ==> Table[i+1] segun la cantidad de XXNULLXX
my $count=0;
#my $position;
my @NULLPLACE;
my @nombre_tabla;

while (defined($documenta->selectElementByContent("XXNULLXX_".$count))){
	#Se selecciona ELEMENTO por CONTENIDO
	$NULLPLACE[$count]=$documenta->selectElementByContent("XXNULLXX_".$count);
	#intentar obtener el nombre de la zona o tabla en que está cada nullplace
	#PRobando con renombrar seccion
	$documenta->renameTable("Table2", "Table2"."_".$count);
	++$count;
}
$documenta->save();

my $document = odfDocument(file => $in_file);
print "Cantidad de elementos a llenar: ".$count."\n";
#Agregar fila a tabla: http://search.cpan.org/dist/OpenOffice-OODoc/OODoc/Text.pod#appendRow%28table_[,_options]%29
#Conseguir cantidad de paginas
###Ahora, teniendo la lista de lugares en el texto en que existe un xxnullxx se itera colocando una nueva fila y revisando la cantidad
#de páginas en el texto
my $place;
my $table;
my $table_name;
my %now_pg;
my $now_cp = $cp;
my $eerr;
my $AX="";
my $BX="";
my $id;
my ($h, $l);
my ($h1, $l1);
#Modelo de tabla: Tabla2_{0...$count-1}
my @lista_tablas = $document -> getTableList();
print "Cantidad de tablas: ".@lista_tablas."\n";
foreach (@lista_tablas) {
	print $_."\n";	
	($h1, $l1) = $document -> getTableSize($_);
	print "Tamaño ".$h1.",".$l1."\n";
}

#Se calcula la cantida de páginas original del documento pasando a pdf y obteniendo la cantidad de páginas.
my $to_pdf=system("unoconv -f pdf ".$in_file);
my $count_pages=`pdfinfo $in_pdf_file | grep ^Pages:| awk -F':' '{print int(\$2)}'`;
$cp=int($count_pages);

#Se realiza la iteracion para cada tabla 'Table2_i' existente y se rellena con filas blancas		
foreach (0..($count-1)) {
	$id=$_;#Id es la variable default de la iteracion 
	$now_cp=0;
	#$place=$NULLPLACE[$id];
	#print $place."\n";
	my $id_tabla =3*$id+2;#la secuencia que corresponde solamente a las tablas 'table2_i'
	my $table = $document -> getTable($id_tabla-1);	#Se activa la tabla correspondiente #Secundario
	my $new_tname = $document -> tableName($id_tabla-1);	#Se extrae nombre de tabla #Secundario
	print $id_tabla."-".$new_tname."\n";
	($h, $l) = $document -> getTableSize($table);#se obtiene el tamaño de tabla
	print "Tamaño ".$h.",".$l."\n";
	$document -> cellValue($table, $h-1, 0,'');	
	while ( $now_cp <= int $cp ) {
		$document -> appendRow($table );
		$document -> save();
		#Pasar a pdf
		$to_pdf=system("unoconv -f pdf ".$in_file);
		$count_pages=`pdfinfo $in_pdf_file | grep ^Pages:| awk -F':' '{print int(\$2)}'`;
		$now_cp=int($count_pages);
		##Recuento de paginas	
		print "La cantidad de páginas es: ".$now_cp."vs original: ".$cp." es entero? :". (isint $now_cp)."\n";
	}
	#Borrar la ultima línea puesta.
	$document -> deleteRow($table, $h)
}

$document ->save("Salida.odt");
