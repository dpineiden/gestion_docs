# -*- coding: utf-8 -*-
def arraydict2string(ADICT,key,label):
  N = len(ADICT)
  pre = '<' + label +'>'
  post = '</' +label + '>'
  valor=''
  valor_html=[]
  for i in range(0,N):
    #Mejorar validación de key en caso de que no exista
    if key in ADICT[i]:
     valor = ADICT[i][key]
     valor_html.append( pre + valor + post )
  texto_html = ''.join(str(e) for e in valor_html)
  return texto_html
    
    