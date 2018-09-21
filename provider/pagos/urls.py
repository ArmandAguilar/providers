from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pagos/$', views.index, name='index'),
    url(r'^pagos/dashboard/$', views.load_dashboard, name='load_dashboard'),
    url(r'^pagos/dashboard/tree/$', views.load_dashboar_tree, name='load_dashboar_tree'),
    url(r'^pagos/update/fechapago/$', views.update_date_pay, name='update_date_pay'),
    url(r'^pagos/update/loadBnk/$', views.load_OperBancks, name='load_OperBancks'),
    url(r'^pagos/update/status/$', views.update_status_pay, name='update_status_pay'),
    url(r'^pagos/cancel/bills/$', views.cancel_pay, name='cancel_pay'),
    url(r'^pagos/form_edit/bill/(?P<id>\d+)/$', views.form_edit_bills, name='form_edit_bills'),
    url(r'^pagos/noproy/$', views.seek_name_proy, name='seek_name_proy'),
    url(r'^pagos/leader/$', views.seek_leader, name='seek_leader'),
    url(r'^pagos/contract/$', views.seek_contract, name='seek_contract'),
    url(r'^pagos/bills/save_edit/$', views.save_edit, name='save_edit'),
    #url(r'^pagos/provider/bnk/$', views., name=''),

]