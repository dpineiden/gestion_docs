from django.conf.urls import patterns, include, url
from django.contrib import admin
from gestion_docs.views import hello, current_datetime, hours_ahead
from procesa_fl.views import envio_sse, envio_exitoso
import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestion_docs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$',hello),
    url(r'^time/$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$',hours_ahead),
    url(r'^admin/',include(admin.site.urls)),
    url(r'^envio_sse/$',envio_sse, name="envio_sse"),
    url(r'^envio_sse/exitoso$',envio_exitoso),
    )
