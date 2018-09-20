from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^banco-proveedor-projecto/$', views.index, name='index'),
]
