for ((i=0;i<=$elementos-1;i++))
do
this_matriz=${matriz[i]} 
awk -v this_matriz="$this_matriz" -v Posicion="$Posicion_ME" -v EQMAT="$Posicion_EQMAT" -F';' '
{if (FNR>=Posicion && FNR<EQMAT) 
{
  if(NR==Posicion) 
  {
    for (p=2;p<=NF;p++) 
    {
    if(length($p) > 0) 
    {
      Matriz[p-1]=$p; 
    }
  }
  };
  Cantidad_Matrices=length(Matriz);
  if(NR>Posicion) 
  {
  k=1;
  for (p=2;p<=Cantidad_Matrices+1;p++){
      if (toupper(Matriz[p-1])~toupper(this_matriz) && $p==1){
	  this_estacion[k]=$1;
	  k=k+1;      
    }
  };
  if(k>1)
	{
	printf this_matriz;
	for (m=1;m<=length(this_estacion);m++)
	  {
		printf ";"this_estacion[m];
	  }
	}
      }
  }
}' $file_sse| awk '{print>>"matriz_estaciones.csv"}';
done