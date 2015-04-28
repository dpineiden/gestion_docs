from django.db import models
from django.forms import ModelForm
from django.forms.fields import FilePathField
from django.contrib.auth.models import User
from formatChecker import ContentTypeRestrictedFileField
import os
import subprocess
from unipath import Path

# Create your models here.
class Cliente(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=100)
    email_contact = models.EmailField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Proyecto(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    client = models.ForeignKey(Cliente)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['code']


class Planilla_SSE(models.Model):
    project = models.ForeignKey(Proyecto, default=1)
    # file_sse= ContentTypeRestrictedFileField(upload_to ="procesa_fl/sse_files",max_upload_size=20971520,content_types=['aplication/xlsx', 'application/xls',],blank=True, null=True)
    file_sse = models.FileField(default='',
                                upload_to="procesa_fl/sse_files")  #En vez de ruta, pasar a un metodo que transforme filename http://stackoverflow.com/questions/2680391/in-django-changing-the-file-name-of-uploading-file
    user_key = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.file_sse.name

    def filename(self):
        return os.path.basename(self.file_sse.name)

    class Meta:
        ordering = ['file_sse', 'upload_date', 'project', 'user_key']


class Planilla_SSE_FORM(ModelForm):
    class Meta:
        model = Planilla_SSE
        fields = ['file_sse', 'project', 'user_key']


# Agregar modelo de archivo derivado del archivo subido anteriormente.

class SSE_Processed_Files(models.Model):
    planilla = models.ForeignKey(Planilla_SSE, default=1)
    folder = models.CharField(max_length=50)
    processed_files = models.FilePathField(recursive=True, max_length=500)
    save_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.folder

    class Meta:
        ordering = ['planilla', 'processed_files', 'save_date']
		
		
