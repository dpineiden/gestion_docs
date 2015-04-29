from django.shortcuts import render, redirect,render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Planilla_SSE, Planilla_SSE_FORM, SSE_Processed_Files
import datetime
import os
import subprocess
from subprocess import Popen, PIPE
import sys
import sh
from unipath import Path

# Create your views here.
# Vista para gestionar los datos de formulario
def envio_sse(request):
	if request.method == 'POST':
		sse = Planilla_SSE_FORM(request.POST, request.FILES)
		if sse.is_valid():
			new_sse = sse.save()
			print "Filename: "+new_sse.filename()
			os.environ['LD_LIBRARY_PATH'] = "/procesa_fl/procesa_sse/"
			print request.FILES['file_sse'].name
			#print new_sse.filename()
			file_sse_name = new_sse.filename()
			bash='/bin/bash ejecutar.sh -f '+file_sse_name#hay que hacer un rename del archivo, antes de guardar
			print bash
			SSE_PATH=os.getcwd()+os.environ['LD_LIBRARY_PATH']
			original_path = os.getcwd()
			#print os.getcwd()+" Path Original"
			os.chdir(SSE_PATH)
			#print os.getcwd()+" Path de Bash scripts"
			os.path.dirname(SSE_PATH)
			sys.path.append(SSE_PATH)
			bash_process=subprocess.Popen( bash , shell = True , stdout = subprocess.PIPE )
			OF, err=bash_process.communicate()
			OUT_FOLDER = OF.rstrip()
			print OUT_FOLDER
			name= OUT_FOLDER.splitlines()
			print name.__len__()
			len_name=name.__len__()
			ZIP_NAME = name[-1]+".zip"
			path_zip=ZIP_NAME
			print "ARchivo ZIP: "+path_zip
			os.chdir(original_path)
			#Rescatar la carpeta en que se guardan los archivos
			#Obtener nombre de archivo zipeado
			#EMAIL o Descarga Directa?>>>Lo segundo es mas sencillo!!!
			request.session['zip_file'] = ZIP_NAME
			return redirect('/envio_sse/exitoso')
	else:
		sse = Planilla_SSE_FORM()
	return render(request,'upload_sse.html',{'form':sse})

def envio_exitoso(request):
	ZIP_NAME=request.session['zip_file']
	print "Archivo zip rescatado: "+ZIP_NAME
	return render(request,'envio_exitoso.html', dict(ZIP_NAME=ZIP_NAME))

def download_zip(request):
	path_to_file="procesa_fl/procesa_sse/salida/"+smart_str(ZIP_NAME)
	#r = request.get(path_to_file, stream = True)
	#f = open(path_to_file, 'wb')
	response = StreamingHttpResponse(streaming_content = path_to_file, mimetype="application/zip")
	response['Content-Disposition'] = "attachment; filename = "+smart_str(path_to_file)
	print path_to_file
	#response['X-Sendfile'] = smart_str(path_to_file)
	return response


def save_path(SSE, FOLDER):
	PFS = SSE_Processed_Files()
	PFS.planilla = SSE
	PFS.folder = FOLDER
	PFS.path = "/procesa_fl/procesa_sse/salida/"+FOLDER
	PFS.save()
	return PFS.folder
	
