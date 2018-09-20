from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^login/make_login/$', views.make_login, name='login_make'),
    url(r'^login/make_logout/$', views.logout, name='logout'),
]
