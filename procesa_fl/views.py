from django.shortcuts import render, redirect,render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Planilla_SSE, Planilla_SSE_FORM
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
			os.environ['LD_LIBRARY_PATH'] = "/procesa_fl/procesa_sse/"
			print request.FILES['file_sse'].name
			file_sse_name = request.FILES['file_sse'].name
			bash='/bin/bash ejecutar.sh -f '+file_sse_name
			print bash
			SSE_PATH=os.getcwd()+os.environ['LD_LIBRARY_PATH']
			original_path = os.getcwd()
			print os.getcwd()+" Path Original"
			os.chdir(SSE_PATH)
			print os.getcwd()+" Path de Bash scripts"
			os.path.dirname(SSE_PATH)
			sys.path.append(SSE_PATH)
			subprocess.call(bash, shell=True)
			os.chdir(original_path)			
			return HttpResponseRedirect('exitoso')	
	else:
		sse = Planilla_SSE_FORM()
	return render(request,'upload_sse.html',{'form':sse})

def envio_exitoso(request):
	return render(request,'envio_exitoso.html')
