from django import forms, models
from django.forms.fields import ChoiceField, ModelChoiceField
from django.gestion_docs.procesa_fl.models import Cliente, Proyecto, Planilla_SSE, Planilla_SSE_FORM
from django.contrib.auth.models import User

class Upload_SSE_form(forms.Form):
	project = forms.ModelChoiceField(queryset = Proyecto.objects.all(),empty_label=None) 
	cliente = forms.ModelChoiceField(queryset = Cliente.objects.all(),empty_label=None) 
	sse_file = forms.FileField(required = True, label='Sube la planilla SSE (excel)')
	
	class Meta:
		model = Planilla_SSE_FORM
	
	def __init__(self, *args, **kwargs):
		super(Upload_SSE_form, self).__init__(*args, **kwargs)
		self.fields['id'].queryset = lista
		
