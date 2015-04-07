from django.shortcuts import render, redirect,render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Planilla_SSE, Planilla_SSE_FORM
import datetime
import subprocess

# Create your views here.
# Vista para gestionar los datos de formulario
def envio_sse(request):
	if request.method == 'POST':
		sse = Planilla_SSE_FORM(request.POST, request.FILES)
		if sse.is_valid():
			new_sse = sse.save()
			#filename=request.FILES['filename']
			bash='. procesa_fl/procesa_sse/test.sh'
			subprocess.call(bash, shell=True)
			return HttpResponseRedirect('<h2>SSE Enviado!</h2>')	
	else:
		sse = Planilla_SSE_FORM()
	return render(request,'upload_sse.html',{'form':sse})
