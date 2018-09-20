"""provider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, }),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    url(r'^', include('login.urls')),
    url(r'^', include('dashboard.urls')),
    url(r'^', include('proveedorprojecto.urls')),
    url(r'^', include('bancoproveedorprojecto.urls')),
    url(r'^', include('facturaproveedor.urls')),
    url(r'^', include('contrato.urls')),
    url(r'^', include('pagos.urls')),
]