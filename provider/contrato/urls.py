from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contrato/$', views.index, name='index'),
    url(r'^contrato/search/provider/$', views.search_provider, name='search_provider'),
    url(r'^contrato/save/$', views.save_data, name='save_data'),
    url(r'^contrato/search/contrato/$', views.search_contract, name='search_contract'),
    url(r'^contrato/edit/search/provider/$', views.search_provider_edit, name='search_provider_edit'),
    url(r'^contrato/edit_save/$', views.save_edit, name='save_edit'),
    url(r'^contrato/delete/$', views.delete_contract, name='delete_contract'),
    url(r'^contrato/verify/$', views.verify_contract, name='verify_contract'),
]
