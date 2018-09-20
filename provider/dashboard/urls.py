from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard/$', views.index, name='dashboard'),
    url(r'^dashboard/provider/add/$', views.add_proveeder, name='add_provider'),
    url(r'^dashboard/provider/search/$', views.search_provider, name='search_provider'),
    url(r'^dashboard/provider/edit/$', views.save_edit_provider, name='provider_edit'),
    url(r'^dashboard/provider/verify/$', views.verify_provider, name='verify_provider'),
]