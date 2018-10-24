from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import pypyodbc as pyodbc
import pymssql
import babel.numbers
import decimal

# Create your views here.
def index(request):
    template = loader.get_template('proveedor_projecto/index.html')
    context = {}
    return HttpResponse(template.render(context,request))
#Here function to serach providers
def search_provider(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        Sql = 'SELECT [Id],[Proveedor],[RFC],[Banco],[Cuenta],[Clabe] FROM [SAP].[dbo].[AAAProveedores] Where [Proveedor] like \'%'+ str(request.POST['txtSearchProvider']) + '%\' or [RFC] like \'%' + str(request.POST['txtSearchProvider']) + '%\''
        try:
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                #here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(value[1]) + '</td>'
                tb += '<td><i class="fa fa-check fa-2x" data-target="#modal-edit" data-toggle="modal" style="cursor:pointer" onclick="set_Provider(' + str(value[0]) + ',\'' + str(value[1]) + '\',\'' + str(value[3]) + '\',\'' + str(value[4]) + '\',\'' + str(value[5]) + '\');"></i></td>'
                tb += '</tr>'

            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
    tb_out = HttpResponse()
    tb_out.write(tb)
    return tb_out
#here function to seek projects
def search_projects(request):
    tb = ''
    Sql = ''
    if request.method == 'POST':
        if request.POST['txtAdmin'] == 'No':
            Sql = 'SELECT [NumProyecto],[NomProyecto],[Estado] FROM [SAP].[dbo].[CatalogoDeProyectos] Where ([NumProyecto] like \'%' + str(request.POST['txtSearchProject']) + '%\' or [NomProyecto] like \'%' + str(request.POST['txtSearchProject']) + '%\') and  (EstadoCompra = \'Activo\')'
        else:
            Sql = 'SELECT [Proyecto],[Concepto] FROM [SAP].[dbo].[ProyectosAdministrativos] Where (Negocio <> \'SHY\') And ([Proyecto] like \'%' + str(request.POST['txtSearchProject']) + '%\' or [Concepto] like  \'%' + str(request.POST['txtSearchProject']) + '%\') '
        try:
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                #here html<button >Launch demo modal</button>
                tb += '<tr>'
                tb += '<td>' + str(int(value[0])) + '.-' + str(value[1]) + '</td>'
                tb += '<td><i class="fa fa-check fa-2x" data-target="#modal-edit" data-toggle="modal" style="cursor:pointer" onclick="set_Proyect(' + str(value[0]) + ',\'' + str(value[1]) + '\')"></i></td>'
                tb += '</tr>'

            conn.commit()
            conn.close()
        except ValueError:
            tb = Sql
        tb_out = HttpResponse()
        tb_out.write(tb)
        return tb_out
#Here we verify is all bill are more than that contrac
def verify_amount_contract(idContract,amount):
    status = 0
    totalContrac = 0
    totalBills = 0
    try:
        #get total of contract
        SqlContracts = 'SELECT [Monto] FROM [SAP].[dbo].[AAAContrato] WHERE [Id] = \'' + str(idContract) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(SqlContracts)
        for data in cur:
            totalContrac = data[0]
        conn.commit()
        conn.close()

        #get total of bills
        SqlBills = 'SELECT [Monto],[IVA] FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE [IdContrato] = \'' + str(idContract) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(SqlBills)
        for dta in cur:
            totalBills += dta[0]
        conn.commit()
        conn.close()
        #Here sum the new amount
        totalBills += amount
        if totalBills > totalContrac:
            #the mount is more than contract
            status = 0
        else:
            #the mount is less than contract
            status = 1
    except ValueError:
        status = 2
    return status
#Here make a realtionsho between Provider & Proy
def save_data(request):
    status = 0
    Total = 0
    verify_status = 0
    if request.method == 'POST':
        try:
            t_amount = float(request.POST['txtMonto'])
            verify_status = verify_amount_contract(request.POST['CboContrato'], t_amount)
            if verify_status == 1:
                Sql = 'INSERT INTO [SAP].[dbo].[AAAProveedorFacturaPoyecto] VALUES (\'' + str(request.POST['CboContrato']) + '\',\'' + str(request.POST['txtIdProvider']) +'\',\'' + str(request.POST['CboLider']) + '\',\'' + str(request.POST['txtIdProject']) + '\',\'' + str(request.POST['txtFactura']) + '\',\'' + str(request.POST['txtMonto']) + '\',\'' + str(request.POST['txtConcepto']) + '\',\'No\',\'' + str(request.POST['txtFechaPago']) + '\',\'' + str(request.POST['txtIva']) + '\',\'' + str(request.POST['txtContable']) + '\')'
                conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
                cur = conn.cursor()
                cur.execute(Sql)
                conn.commit()
                conn.close()
                #Here send data for incress pasivo with iva
                if  int(request.POST['txtIdProject']) > 100:
                    if str(request.POST['txtContable']) == 'Si':
                        Total = float(request.POST['txtMonto']) + float(request.POST['txtIva'])
                        nsql = increse_charge(request.POST['txtIdProject'], Total)
                    else:
                        val = 0
                status = 1
            elif verify_status == 0:
                status = 2
            elif verify_status == 2:
                status = 0
        except ValueError:
            status = 0

    return HttpResponse(status, content_type="application/liquid charset=utf-8;")

def load_cbo_leads(request):
    data_text = '<option value="0" selected>--------Lider de Proyecto-------</option>'

    try:
        Sql = 'Select Id,Nombre,Apellidos From [Northwind].[dbo].[Usuarios] Where (CobranzaPerfil =\'Admin\' or CobranzaPerfil=\'User\') and (Departamento <> \'Baja\') order by Nombre'
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQLNORTHWIND)
        cur = conn.cursor()
        cur.execute(Sql)
        for value in cur:
            #data_text += '<option value="' + str(value[0]) + '">' + str(value[1])  + ' ' + str(value[2].encode("iso-8859-1")) + '</option>'
            apellidos = value[2].decode("iso-8859-1")
            data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + ' ' + str(apellidos.encode("iso-8859-1")) + '</option>'
        conn.commit()
        conn.close()
    except ValueError:
            data_text = ''
    cbo_data = HttpResponse()
    cbo_data.write(data_text)
    return cbo_data

def load_cbo_contract(request):
    amount = 0
    total = 0
    data_text = '<option value="0" selected>--------Contratos-------</option>'
    try:
        Sql = 'SELECT [Id],[Contrato],[Monto],[Iva] FROM [SAP].[dbo].[AAAContrato] Where [IdProveedor] = \'' + str(request.POST['txtIdProvider']) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(Sql)
        for value in cur:
            total = float(value[2]) + float(value[3])
            amount = babel.numbers.format_currency(str(total), 'USD', locale='en_US')
            data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + ' x ' + str(amount) + '</option>'
        conn.commit()
        conn.close()
    except ValueError:
            data_text = ''
    cbo_data = HttpResponse()
    cbo_data.write(data_text)
    return cbo_data
#Here update bkn of providers
def save_edit_banco(request):
    status = 0
    if request.method == 'POST':
        try:
            Sql = 'UPDATE [SAP].[dbo].[AAAProveedores] SET [Banco] = \'' + str(request.POST['txtBanco']) + '\',[Cuenta] = \'' + str(request.POST['txtCuenta']) + '\',[Clabe] = \'' + str(request.POST['txtClabe']) + '\' WHERE Id=\'' + str(request.POST['txtIdProvider']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            conn.commit()
            conn.close()
            status = 1
        except ValueError:
            status = 0
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")

#Here we make code to adapter the old system with the new system
# function syc the table
def increse_charge(NumProy,mount):
    status = 0
    NoProyect = 0
    amountDB = 0
    totalamount = 0
    #Step 1 : We need know if exit the proyect in RV-Pasivos
    ##Step 1.1 : Get proyect
    try:
        sql  = 'SELECT [NumProyecto],[Pasivos] FROM [SAP].[dbo].[RV-Pasivos] Where [NumProyecto] = \'' + str(NumProy) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            NoProyect = value[0]
            amountDB = value[1]
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        status = 0

    #Step 1.2 If proyect exist sum the new mount
    if NoProyect > 0:
        try:
            totalamount  = float(mount) + float(amountDB)
            sql = 'UPDATE [SAP].[dbo].[RV-Pasivos] SET [NumProyecto] = \'' + str(NumProy) + '\',[Pasivos] = \'' + str(totalamount) + '\' WHERE NumProyecto = \'' + str(NumProy) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
        except pymssql.Error as e:
            status = 0
    ##else create the new proyect with  mount
    else:
        try:
            sql = 'INSERT INTO[SAP].[dbo].[RV-Pasivos] VALUES(\'' + str(NumProy) + '\', \'' + str(mount) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
        except pymssql.Error as e:
            status = 0
    return status
