#Obtener lista de parametros
 sed 's/(/;(/g' parametros.dat | awk -F';' '{
 expr="/total y disuelto/";
 if ($1 ~ exprx) 
 {
  split($1,param," ");
  if(length(param[1])>1){ 
    print param[1] " total";
    print param[1], " disuelto";}
  } 
  else if ($1 !~ expr) {
    print $1
    }
 }' > parametros_final.dat
 
#Obtener lista de laboratorios asociados a parametros

sed 's/(/;(/g' parametros.dat | awk -F';' '{
expr="/total y disuelto/";
lab=substr($2,2,length($2)-2);
if ($1 ~ exprx) 
  {
  split($1,param," ");
  if(length(param[1])>1)
    {
    print lab;print lab;
    }
  } 
else if ($1 !~ expr) 
  CEA{
  print lab
  }
}'|sed 's/)//g'|sed 's/-//g' > laboratorios.dat
