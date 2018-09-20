from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^proveedor-projecto/$', views.index, name='index'),
    url(r'^proveedor-projecto/provider/search/$', views.search_provider, name='search_provider'),
    url(r'^proveedor-projecto/project/search/$', views.search_projects, name='search_project'),
    url(r'^proveedor-projecto/save/$', views.save_data, name='save_project'),
    url(r'^proveedor-projecto/cbo_lider/$', views.load_cbo_leads, name='load_cbo_leads'),
    url(r'^proveedor-projecto/cbo_contract/$', views.load_cbo_contract, name='load_cbo_contract'),
    url(r'^proveedor-projecto/save_edit_banco/$', views.save_edit_banco, name='save_edit_banco'),
]
