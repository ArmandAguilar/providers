from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import pypyodbc as pyodbc
import pymssql

# Create your views here.
def index(request):
    template = loader.get_template('dashboard/dashboard.html')
    context = {}
    return HttpResponse(template.render(context,request))

#here save data
def add_proveeder(request):
    status = 0
    if  request.method == 'POST':
        try:
            Sql = 'INSERT INTO [SAP].[dbo].[AAAProveedores] VALUES (\'' + str(request.POST['txtProvider']) + '\',\'' + str(request.POST['txtRFC']) + '\' ,\'' + str(request.POST['txtBanco']) + '\',\'' + str(request.POST['txtSucursal']) + '\',\'' + str(request.POST['txtCuenta']) + '\',\' ' + str(request.POST['txtClabe']) + '\',\'' + str(request.POST['txtReferencia']) + '\',\'0\',\'0\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1
        except ValueError:
            status = 0
    return HttpResponse(status,content_type="application/liquid charset=utf-8;")

#search providers
def search_provider(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        Sql = 'SELECT [Id],[Proveedor],[RFC],[Banco],[Sucursal],[Cuenta],[Clabe],[Referencia] FROM [SAP].[dbo].[AAAProveedores] Where [Proveedor] like \'%'+ str(request.POST['txtSearchProvider']) + '%\' or [RFC] like \'%' + str(request.POST['txtSearchProvider']) + '%\''
        try:
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                #here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(value[1])+ '</td>'
                tb += '<td><i class="fa fa-cog fa-2x"></i></td>'
                tb += '<td><i class="fa fa-pencil fa-2x" data-target="#modal-edit" data-toggle="modal" style="cursor:pointer" onclick="setValuesEdit(' + str(value[0]) + ',\'' + str(value[1])  + '\',\'' + str(value[2]) + '\',\'' + str(value[3]) + '\',\'' + str(value[4]) + '\',\'' + str(value[5]) + '\',\'' + str(value[6]) + '\',\'' + str(value[7]) + '\');"></i></td>'
                tb += '</tr>'

            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
    tb_out = HttpResponse()
    tb_out.write(tb)
    return tb_out
#Save edit provider
def save_edit_provider(request):
    status = 0
    Sql = ''
    if request.method == 'POST':
        try:
            Sql = 'UPDATE [SAP].[dbo].[AAAProveedores] SET [Proveedor] = \'' + str(request.POST['txtProviderEdit']) + '\' ,[RFC] = \'' + str(request.POST['txtRFCEdit']) + '\',[Banco] = \'' + str(request.POST['txtBancoEdit']) + '\',[Sucursal] = \'' + str(request.POST['txtSucursalEdit']) + '\',[Cuenta] = \'' + str(request.POST['txtCuentaEdit']) + '\',[Clabe] = \'' + str(request.POST['txtClabeEdit']) + '\',[Referencia] = \'' + str(request.POST['txtReferenciaEdit']) + '\' WHERE Id = \'' + str(request.POST['txtEditId']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1
        except ValueError:
            status = 0
    return HttpResponse(status,content_type="application/liquid charset=utf-8;")
#Verify provider
def verify_provider(request):
    status = 0
    Sql = ''
    if request.method == 'POST':
        try:
            Sql = 'SELECT [Proveedor] FROM [SAP].[dbo].[AAAProveedores] Where [Proveedor] = \'' + str(request.POST['txtProvider']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                if str(value[0]) == str(request.POST['txtProvider']):
                    status = 1
            conn.commit()
            conn.close()
        except ValueError:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")

