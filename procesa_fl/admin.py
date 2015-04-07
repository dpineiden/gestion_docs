from django.contrib import admin
from procesa_fl.models import Planilla_SSE, Proyecto, Cliente
# Register your models here.

class Planilla_SSE_Admin(admin.ModelAdmin):
	list_display = ('file_sse','upload_date','project', 'user_key')
	list_filter= ('upload_date',)
	date_hierarchy = 'upload_date'
	ordering = ('-upload_date',)
	
admin.site.register(Cliente)
admin.site.register(Proyecto)
admin.site.register(Planilla_SSE,Planilla_SSE_Admin)


