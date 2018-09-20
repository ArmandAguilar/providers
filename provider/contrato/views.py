from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import pypyodbc as pyodbc
import pymssql


# Create your views here.
def index(request):
    template = loader.get_template('contrato/index.html')
    context = {}
    return HttpResponse(template.render(context,request))

#here seek all proviider
def search_provider(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        Sql = 'SELECT [Id],[Proveedor],[RFC] FROM [SAP].[dbo].[AAAProveedores] Where [Proveedor] like \'%' + str(request.POST['txtSearchProvider']) + '%\' or [RFC] like \'%' + str(request.POST['txtSearchProvider']) + '%\''
        try:
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                # here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(value[1]) + '</td>'
                tb += '<td><i class="fa fa-check fa-2x"  style="cursor:pointer" onclick="set_Provider(' + str(value[0]) + ',\'' + str(value[1]) + '\');"></i></td>'
                tb += '</tr>'

            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
    tb_out = HttpResponse()
    tb_out.write(tb)
    return tb_out
#save data
def save_data(request):
    status = 0
    if request.method == 'POST':
        try:
            Sql = 'INSERT INTO [SAP].[dbo].[AAAContrato] VALUES (\'' + str(request.POST['txtIdProveedor']) + '\',\'' + str(request.POST['txtContrato']) + '\',\'' + str(request.POST['txtMonto']) + '\',\'' + str(request.POST['txtIVA']) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1

        except ValueError:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#serach contract
def search_contract(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        try:
            Sql = 'SELECT [Id],[IdProveedor],[Contrato],[Monto],[Iva] FROM [SAP].[dbo].[AAAContrato] where Contrato Like \'%'+ str(request.POST['txtSearchContrato']) + '%\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                # here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(value[2]) + '</td>'
                tb += '<td><i class="fa fa-edit fa-2x"  data-target="#modal-edit" data-toggle="modal" style="cursor:pointer" onclick="setEdit(\'' + str(value[0]) + '\',\'' + str(value[1]) + '\',\'' + str(value[2]) + '\',' + str(value[3]) + ',' + str(value[4]) + ');"></i></td>'
                tb += '<td><i class="fa fa-close fa-2x"  data-target="#modal-delete" data-toggle="modal" style="cursor:pointer" onclick="setDelete(' + str(value[0]) + ',' + str(value[1]) + ');"></i></td>'
                tb += '</tr>'
            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
    tb_out = HttpResponse()
    tb_out.write(tb)
    return tb_out
#seacrh provier for modalbox
def search_provider_edit(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        Sql = 'SELECT [Id],[Proveedor],[RFC] FROM [SAP].[dbo].[AAAProveedores] Where [Proveedor] like \'%'+ str(request.POST['txtSearchProviderEdit']) + '%\' or [RFC] like \'%' + str(request.POST['txtSearchProviderEdit']) + '%\''
        try:
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                #here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(value[1])+ '</td>'
                tb += '<td><i class="fa fa-check fa-2x" style="cursor:pointer" onclick="setIdProviderEdit(' + str(value[0]) + ',\'' + str(value[1]) + '\')"></i></td>'
                tb += '</tr>'

            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
    tb_out = HttpResponse()
    tb_out.write(tb)
    return tb_out
#Here save data edit
def save_edit(request):
    status = 0
    Sql = ''
    if request.method == 'POST':
        try:
            Sql = 'UPDATE [SAP].[dbo].[AAAContrato] SET [IdProveedor] = \'' + str(request.POST['txtIdProviderEdit']) + '\',[Contrato] = \'' + str(request.POST['txtEditContrato']) + '\',Monto=\'' + str(request.POST['txtMontoEdit']) + '\',Iva = \'' + str(request.POST['txtIvaEdit']) + '\' WHERE Id =\'' + str(request.POST['txtEditId']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1

        except ValueError:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#Here Detele
def delete_contract(request):
    status = 0
    Sql=''
    SqlBill = ''
    if request.method == 'POST':
        try:
            #DELETE FROM [SAP].[dbo].[AAAContrato] WHERE Id=''
            #DELETE FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE IdProveedor = '' and IdContrato = ''
            #zero apply the discount before to delete all the bills
            SqlBill = 'Select [NumProyecto],[Monto] FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE IdProveedor = \'' + str(request.POST['txtIdProviderDelete']) + '\' and IdContrato = \'' + str(request.POST['txtIdContractDelete']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(SqlBill)
            for value in cur:
                decrees_charge(value[0], value[1])
            conn.commit()
            conn.close()
            #Fisrt delete all registre of [AAAProveedorFacturaPoyecto]
            Sql = 'DELETE FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE IdProveedor = \'' + str(request.POST['txtIdProviderDelete']) + '\' and IdContrato = \'' + str(request.POST['txtIdContractDelete']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            #Second delete al register of [AAAContrato]
            Sql = 'DELETE FROM [SAP].[dbo].[AAAContrato] WHERE Id=\'' + str(request.POST['txtIdContractDelete']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1

        except ValueError:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#Verfy contract
def verify_contract(request):
    status = 0
    if request.method == 'POST':
        try:
            Sql = 'SELECT [Contrato] FROM [SAP].[dbo].[AAAContrato] Where [Contrato] = \'' + str(request.POST['txtContrato']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                if request.POST['txtContrato'] == value[0]:
                    status = 1
            conn.commit()
            conn.close()
        except:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")

#Here we make code to adapter the old system with the new system
# function syc the table

def decrees_charge(NumProy,amount):
    status = 0
    amountDB = 0
    totalamount = 0

    #Get the data of RV-Pasivos
    try:
        sql  = 'SELECT [NumProyecto],[Pasivos] FROM [SAP].[dbo].[RV-Pasivos] Where [NumProyecto] = \'' + str(NumProy) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            amountDB = value[1]
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        status = 0

    #discount the amount
    totalamount = float(amountDB) - float(amount)

    #Here update the amount in RV-PASIVOS
    try:
        if totalamount < 0:
            totalamount = 0
        sql = 'UPDATE [SAP].[dbo].[RV-Pasivos] SET [NumProyecto] = \'' + str(NumProy) + '\',[Pasivos] = \'' + str(totalamount) + '\' WHERE NumProyecto = \'' + str(NumProy) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        status = 0
    return status