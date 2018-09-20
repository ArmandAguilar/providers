from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^factura-proveedor/$', views.index, name='index'),
]
