for ((i=0;i<=$Cant_lab-1;i++))
  do
  # <nombre_laboratorio> es la variable que se ingresa para buscar segun la columna N_Lab
    Nombre_lab=${Laboratorios[i]}
    for ((j=0;j<=$N_matrices-1;j++))
      do
      #SI Laboratorio es CEA-->generar resumen-->FL33
      #Se genera un archivo con nombre <laboratorio>.csv
      #Con estructura:
      # matriz - cantidad - total_parametro - replicas por estacion
      #Para esto se capturan las variables de <nombre lab> <matriz-cols> y se usan los valores de Nfilas y NColLab
      #Un array de bash se puede ingresar en awk de la siguiente manera:
      # awk -v var="${test[*]}" '{n=split(var,test," ");print test[2]}' SSE_matriz.csv
      # <matriz-cols> es el arreglo que se ingresa para buscar solamente las columnas que corresponden a esa matriz
      #Entrega un string con el nombre y los indices:
      matriz_cols=$(grep ${this_matrices[j]} columnas_matriz.csv | sed 's/_/ /g' )
      #dentro del awk:
      #  Separo el nombre de matriz de cols y obtengo los indices de las columnas, itero en la cantidad de ellas
      # las sumo, saco un promedio y obtengo el floor entero  del promedio 'replica=int(a/b)'
      #Cada nueva variable en awk se debe ingresar antecediendo -v
      #awk -v var="${test[*]}" -v group="$Grupo" '{n=split(var,test," ");print test[2], group}' SSE_matriz.csv
      echo $Nombre_lab $matriz_cols
      #Si laboratorio es de los otros--->Generar resumen-->R08
      done
  done