from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import pypyodbc as pyodbc
import pymssql
import calendar
import datetime
import simplejson as json
import babel.numbers
import decimal

# Create your views here.
def index(request):
    template = loader.get_template('pagos/index.html')
    context = {}
    return HttpResponse(template.render(context,request))

#here get all data's bill for mouth
def bills_json(month,year):

    BillsJson = ''
    Key = 0
    BillsJson = '{"Bills":['
    dateMonthStart = "%s-%s-01" % (year, month)
    if month > 1:
        dateMonthEnd = "%s-%s-%s" % (year, month, calendar.monthrange(year, month)[1])

    else:
        dateMonthEnd = str(year) + '-01-31'

    sql ='SELECT [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Id]'#0
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdContrato]'#1
    sql += ',[SAP].[dbo].[AAAContrato].[Contrato]'#2
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdProveedor]'#3
    sql += ',[SAP].[dbo].[AAAProveedores].[Proveedor]'#4
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdLider]'#5
    sql += ',[Northwind].[dbo].[Usuarios].[Nombre]'#6
    sql += ',[Northwind].[dbo].[Usuarios].[Apellidos]'#7
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[NumProyecto]'#8
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Factura]'#9
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Monto]'#10
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Concepto]'#11
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[FechaPago]'#12
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Estado]'#13
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Iva]'#14
    sql += ',[SAP].[dbo].[AAAContrato].[Monto]'#15
    sql += ',[SAP].[dbo].[AAAContrato].[Iva]'#16
    sql += ',[SAP].[dbo].[AAAProveedores].[Banco]'  # 17
    sql += ',[SAP].[dbo].[AAAProveedores].[Cuenta]'  # 18
    sql += ',[SAP].[dbo].[AAAProveedores].[Clabe]'  # 19
    sql += 'FROM'
    sql += '[SAP].[dbo].[AAAProveedorFacturaPoyecto],'
    sql += '[SAP].[dbo].[AAAProveedores],'
    sql += '[SAP].[dbo].[AAAContrato],'
    sql += '[Northwind].[dbo].[Usuarios]'
    sql += 'Where  ([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdProveedor = [SAP].[dbo].[AAAProveedores].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdContrato = [SAP].[dbo].[AAAContrato].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdLider = [Northwind].[dbo].[Usuarios].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago >= \'' + str(dateMonthStart) + '\' and [SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago <= \'' + str(dateMonthEnd) + '\')'

    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            date_small = str(value[12]).split(" ")
            ds = str(date_small[0]).split("-")
            date_format = str(int(ds[2])) + '/' + str(int(ds[1])) + '/' +  str(ds[0])
            amountBills = get_balance(value[1])
            amountBillsTotal = (float(value[15]) + float(value[16])) - float(amountBills)
            BillsJson += '{"Id":'+ str(value[0]) + ',"IdContrato":' + str(value[1]) + ',"Contrato":"' + str(value[2]) + '","IdProveedor":' + str(value[3]) + ',"Proveedor":"' + str(value[4]) + '","IdLider":' + str(value[5]) + ',"Nombre":"' + str(value[6]) + '","NumProyecto":' + str(value[8]) + ',"Factura":"' + str(value[9]) + '","Monto":' + str(value[10]) + ',"Concepto":"' + str(value[11]) + '","FechaPago" : "' + str(date_format) + '","Estado":"' + str(value[13])+ '","Iva":' + str(value[14]) + ',"Contrato_Monto":' + str(value[14]) + ',"Contrato_IVA":' + str(value[15]) + ',"Banco":"' + str(value[17]) + '","Cuenta":"' + str(value[18]) + '","Clabe":"' + str(value[19]) + '","Balance":' + str(amountBillsTotal) + '},' + '\n'
            Key = 1
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        vars = 'SQL Error: ' + str(e)
    temp = len(BillsJson)
    BillsJson = BillsJson[:temp - 2]
    BillsJson += ']}'
    if Key > 0:
        data = json.loads(BillsJson)
    else:
        BillsJsonVacio = ''
        BillsJsonVacio = '{"Bills":['
        BillsJsonVacio += '{"Id":0,"IdContrato":0,"Contrato":"000","IdProveedor":0,"Proveedor":"AAA","IdLider":0,"Nombre":"AAA","NumProyecto":0,"Factura":"000","Monto":0,"Concepto":"AA","FechaPago" : "0000-00-00","Iva":0}' + '\n'
        BillsJsonVacio += ']}'
        data = json.loads(BillsJsonVacio)
    return data

#here view to edit pay
def form_edit_pay(request):
    template = loader.get_template('pagos/editar_pagos.html')
    context = {}
    return HttpResponse(template.render(context, request))

#Here fill al gaps bettwen dates
def fill_row_with_data(dJson,seekValue):
    colorbox = 'bg-gray'
    payed = 0.0
    data = ''
    data += '<div class ="row text-center">'
    for vals in dJson['Bills']:

        if vals['FechaPago'] == seekValue:
            colorbox = 'bg-gray'
            pay = babel.numbers.format_currency(str(vals['Monto']), 'USD', locale='en_US')
            iva = babel.numbers.format_currency(str(vals['Iva']), 'USD', locale='en_US')
            btwiva = float(vals['Monto']) + float(vals['Iva'])
            bill_whit_iva = babel.numbers.format_currency(str(btwiva), 'USD', locale='en_US')
            EContract = float(vals['Contrato_Monto']) + float(vals['Contrato_IVA'])
            contract_whit_iva = babel.numbers.format_currency(str(EContract), 'USD', locale='en_US')
            balance = babel.numbers.format_currency(str(vals['Balance']), 'USD', locale='en_US')
            #Here we evalutes all opcion fo set the color
            if str(vals['Factura']) == 'Provisionar':
                colorbox = 'bg-danger'
            if str(vals['Factura']) == 'Provisionar' and float(vals['Iva'])  == 0:
                colorbox = 'bg-gray'
            if str(vals['Estado']) == 'Si' and float(vals['Iva'])  > 0:
                colorbox = 'bg-primary'
                payed = bill_whit_iva
            if str(vals['Estado']) == 'Si' and float(vals['Iva']) == 0:
                colorbox = 'bg-success'
                payed = bill_whit_iva
             #Here print the data
            data += '  <div class ="row text-left text-bold"><div class ="col-sm-12">'
            data += '      <div class ="panel media pad-all ' + str(colorbox) + '">'
            data += '          <div class ="media-body">'
            data += '              <p class ="mar-no">Lider:' + str(vals['Nombre']) + '</p>'
            data += '              <p class ="mar-no">NoProyecto:' + str(vals['NumProyecto']) + '</p>'
            data += '              <p class ="mar-no">' + str(vals['Proveedor']) + '</p>'
            data += '              <p class ="mar-no">Contrato:' + str(contract_whit_iva) + '</p>'
            data += '              <p class ="mar-no">Factura:' + str(vals['Factura']) + '</p>'
            data += '              <p class ="mar-no">Monto:' + str(pay) + '</p>'
            data += '              <p class ="mar-no">Iva:' + str(iva) + '</p>'
            data += '              <p class ="mar-no">Total:' + str(bill_whit_iva) + '</p>'
            data += '              <p class ="mar-no">Pagado:' + str(payed) + '</p>'
            data += '              <p class ="mar-no">Saldo:' + str(balance) + '</p>'
            data += '              <p class ="mar-no">&nbsp;</p>'
            if str(vals['Estado']) == 'Si':
                data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\''  + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk('+ str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div></div>'
            else:
                data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\'' + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk(' + str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(vals['Id']) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills" data-toggle="modal" onclick="setIdForPayStatus(' + str(vals['Id']) + ',\'' + str(vals['Factura']) + '\',' + str(vals['Monto']) + ',' + str(vals['Iva']) + ',0)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(vals['Id']) + ',1,' + str(vals['Monto']) + ',' + str(vals['NumProyecto']) + ');"></div></div>'
            data += '          </div>'
            data += '      </div>'
            data += '  </div></div>'
    data += '</div>'
    return data
#here we calculate Total of each week
def total_for_week(startDate,endDate):
    total = '0.0'
    try:
        sql = 'SELECT sum([Monto]) As Total FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] Where ([SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago >= \'' + str(startDate) + '\' and [SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago <= \'' + str(endDate) + '\')'
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            total = str(value[0])
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        total = 'SQL Error: ' + str(e)
    return total
#Here make update for
def update_date_pay(request):
    status = 0
    if request.method == 'POST':
        try:
            sql = 'UPDATE [SAP].[dbo].[AAAProveedorFacturaPoyecto] SET [FechaPago] = \'' + str(request.POST['txtFechaPago']) + '\' WHERE Id=\'' + str(request.POST['txtIdDate']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            status = 1
        except pymssql.Error as e:
            status = 'SQL Error: ' + str(e)
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#Here set Bill Vs OperBank
def load_OperBancks(request):
    Select_Option = ''
    Select_Option += '<select id="CboBnk" name="CboBnk">'
    if request.method == 'POST':
        try:
            sql = 'SELECT [Id_Oper],[SaldoRestante],[IvaRestante],[Concepto] FROM [SAP].[dbo].[AAAOperacionesPasivosVsBancos] Where [SaldoRestante] > 0  and CategoriaCargo = \'TERCEROS PROYECTO\''
            #sql = 'SELECT [Id_Oper],[Cargo],[Iva],[Cuenta],[Concepto] FROM [SAP].[dbo].[OperacionesConsulting] Where Cargo > 0 and Fecha >= \'2018-07-01\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            for val in cur:
                IVA = babel.numbers.format_currency(str(val[2]), 'USD', locale='en_US')
                MONTO = babel.numbers.format_currency(str(val[1]), 'USD', locale='en_US')
                Select_Option += '<option value="' + str(val[0]) + '">' + str(val[0]) + '|' + str(MONTO)  + '|' + str(IVA) + '|' + str(val[3]) + '</option>'
            conn.commit()
            conn.close()
        except:
            Select_Option += '<option>--- Error ----</option>'

    Select_Option += '</select>'
    out = HttpResponse()
    out.write(Select_Option)
    return out

def update_status_pay(request):
    status = 0
    if request.method == 'POST':
        try:
            #Insert in [AAAPasivoConsulting]
            SqlInsert = 'INSERT INTO [SAP].[dbo].[AAAPasivoConsulting] VALUES (\'' + request.POST['CboBnk'] + '\',\'' + request.POST['txtFactura'] + '\',\'' + request.POST['txtImporte'] + '\',\'' + request.POST['txtIva'] + '\',\'' + str(request.POST['txtIdBills']) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(SqlInsert)
            conn.commit()
            conn.close()
            #Update in [AAAProveedorFacturaPoyecto]
            sql = 'UPDATE [SAP].[dbo].[AAAProveedorFacturaPoyecto] SET [Estado] = \'Si\' WHERE Id=\'' + str(request.POST['txtIdBills']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            status = 1
        except pymssql.Error as e:
            status = 'SQL Error: ' + str(e)
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#Here cancel bills
def cancel_pay(request):
    status = 0
    if request.method == 'POST':
        decrees_charge(request.POST['txtNumProy'],request.POST['txtMonto'])
        try:
            sql = 'DELETE FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE Id = \'' + str(request.POST['txtIdCancel']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            status = 1
        except pymssql.Error as e:
            status = 'SQL Error: ' + str(e)
    return HttpResponse(status, content_type="application/liquid charset=utf-8;")
#edit bills
def form_edit_bills(request,id):
    template = loader.get_template("pagos/editar_pago.html")

    #Here get all data for the form
    sql = ''
    sql += 'SELECT [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Id]' #0
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdContrato]'#1
    sql += ', [SAP].[dbo].[AAAContrato].[Contrato]' #2
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdProveedor]'#3
    sql += ', [SAP].[dbo].[AAAProveedores].[Proveedor]'#4
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdLider]'#5
    sql += ', [Northwind].[dbo].[Usuarios].[Nombre]'#6
    sql += ', [Northwind].[dbo].[Usuarios].[Apellidos]'#7
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[NumProyecto]'#8
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Factura]'#9
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Monto]'#10
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Concepto]'#11
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[FechaPago]'#12
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Iva]'  # 13
    sql += 'FROM'
    sql += '[SAP].[dbo].[AAAProveedorFacturaPoyecto],'
    sql += '[SAP].[dbo].[AAAProveedores],'
    sql += '[SAP].[dbo].[AAAContrato],'
    sql += '[Northwind].[dbo].[Usuarios]'
    sql += 'Where([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdProveedor = [SAP].[dbo].[AAAProveedores].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdContrato =[SAP].[dbo].[AAAContrato].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdLider =[Northwind].[dbo].[Usuarios].Id) and [SAP].[dbo].[AAAProveedorFacturaPoyecto].Id = \'' + str(id) + '\''

    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:

            context = {
                'id': value[0],
                'idcontrato':value[1],
                'contrato':value[2],
                'idproveedor':value[3],
                'proveedor':value[4],
                'idlider':value[5],
                'nombre':value[6],
                'numproyecto':value[8],
                'factura':value[9],
                'monto':value[10],
                'iva': value[13],
                'concepto':value[11],
                'fechapago':value[12].strftime("%Y-%m-%d"),
            }
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        total = 'SQL Error: ' + str(e)

    return HttpResponse(template.render(context, request))
#Here seek name of proyect
def seek_name_proy(request):
    NomProy = '0'
    if request.method == 'POST':
        #
        try:
            sql = 'SELECT [NomProyecto] FROM [SAP].[dbo].[CatalogoDeProyectos] Where NumProyecto = \'' + str(request.POST['txtNoProy']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            for value in cur:
                NomProy = str(value[0])
            conn.commit()
            conn.close()
        except pymssql.Error as e:
            total = 'SQL Error: ' + str(e)
    out = HttpResponse()
    out.write(NomProy)
    return out
#Here seek Lider
def seek_leader(request):
    data_text = ''
    if request.method == 'POST':
        try:
            Sql = 'Select Id,Nombre From [Northwind].[dbo].[Usuarios] Where (CobranzaPerfil =\'Admin\' or CobranzaPerfil=\'User\') and (Departamento <> \'Baja\') order by Nombre'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQLNORTHWIND)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                if value[0] == str(request.POST['txtidLeader']):
                    data_text += '<option value="' + str(value[0]) + '" selected>' + str(value[1])  + '</option>'
                else:
                    data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + '</option>'
            conn.commit()
            conn.close()
        except ValueError:
            data_text = 'i'
        cbo_data = HttpResponse()
        cbo_data.write(data_text)
    return cbo_data
#Here seek contrato
def seek_contract(request):
    data_text = ''
    if request.method == 'POST':
        try:
            Sql = 'SELECT [Id],[Contrato] FROM [SAP].[dbo].[AAAContrato] Where [IdProveedor]=\'' + str(request.POST['txtIdProvider']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                if value[0] == str(request.POST['txtIdContract']):
                    data_text += '<option value="' + str(value[0]) + '" selected>' + str(value[1]) + '</option>'
                else:
                    data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + '</option>'
            conn.commit()
            conn.close()
        except ValueError:
            data_text = ''
        cbo_data = HttpResponse()
        cbo_data.write(data_text)
    return cbo_data
#Here save edit datas
def save_edit(request):
    status = 0
    if request.method == 'POST':
        try:
            # Here get data of old bills
            oldAmount = 0
            oldTax = 0
            oldTotalBill = 0
            sqlOldMountBills = 'SELECT [Monto],[Iva] From [SAP].[dbo].[AAAProveedorFacturaPoyecto] WHERE [Id] = \'' + str(request.POST['txtId']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sqlOldMountBills)
            for Vdata in cur:
                oldAmount = Vdata[0]
                oldTax = Vdata[1]
            conn.commit()
            conn.close()
            oldTotalBill = oldAmount  + oldTax

            #Get total Pasive
            totalPasive = 0
            sqlOldMountPasive = 'SELECT [Pasivos] From [SAP].[dbo].[RV-Pasivos] WHERE [NumProyecto] = \'' + str(request.POST['txtIdProject']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sqlOldMountPasive)
            for Pdata in cur:
                totalPasive = Pdata[0]
            conn.commit()
            conn.close()

            #Here we make us the rest bettween Pasive total - old bill amount
            pasivo_actual = 0
            pasivo_actual = totalPasive - oldTotalBill
            pasivo_actual += float(request.POST['txtMonto']) + float(request.POST['txtIva'])
            #here Sum to pasive  the new change in the bill


            #Here update the new pasive
            sqlUdatePasive = 'UPDATE [SAP].[dbo].[RV-Pasivos] SET [Pasivos] = \''  + str(pasivo_actual) + '\' WHERE [NumProyecto] = \'' + str(request.POST['txtIdProject']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sqlUdatePasive)
            conn.commit()
            conn.close()

            # Here make update bill
            sql = ''
            sql += 'UPDATE [SAP].[dbo].[AAAProveedorFacturaPoyecto] '
            sql += ' SET [IdContrato] = \'' + str(request.POST['CboContrato']) + '\''
            sql += ', [IdProveedor] = \'' + str(request.POST['txtIdProvider']) + '\''
            sql += ', [IdLider] = \'' + str(request.POST['CboLider']) + '\''
            sql += ', [NumProyecto] = \'' + str(request.POST['txtIdProject']) + '\''
            sql += ', [Factura] = \'' + str(request.POST['txtFactura']) + '\''
            sql += ', [Monto] = \'' + str(request.POST['txtMonto']) + '\''
            sql += ', [Iva] = \'' + str(request.POST['txtIva']) + '\''
            sql += ', [Concepto] = \'' + str(request.POST['txtConcepto']) + '\''
            sql += ', [FechaPago] = \'' + str(request.POST['txtFechaPago']) + '\''
            sql += ' WHERE [Id] = \'' + str(request.POST['txtId']) + '\''

            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            status = 1
        except pymssql.Error as e:
            status = 0
    data = HttpResponse()
    data.write(status)
    return data

#Here draw the dashboard calendar
def load_dashboard(request):
    head_date = ''
    if request.method == 'POST':
        mount = int(request.POST['CboMes'])
        year = int(request.POST['txtYear'])
    else:
        #mount = 7
        #year = 2018
        time_now = datetime.datetime.now()
        year = time_now.year
        mount = int(time_now.month)
    Fecha = '00/00/0000'
    contadorCols = []
    k = 0
    cal = calendar.monthcalendar(year, mount)
    dataJson = bills_json(mount,year)
    head_date += '<div class ="row text-center">'
    cols_x = 0
    cols_xx = 3
    for cal_value in cal:
        for dia in cal_value:
            if dia > 0:
                DayWeek = datetime.date(year, mount, dia).strftime("%A")
                if DayWeek == 'Friday':
                    cols_x += 1
    if cols_x > 4:
        cols_xx = 2
    for cal_value in cal:
        for dia in cal_value:
            #Format here the date for dias empty
            if dia == 0:
                Fecha = '00/00/0000'
            else:
                Fecha = str(dia) + '/'  + str(mount)  + '/' +  str(year)
            #here we see if is Sat or Sun
            if dia > 0:
                DayWeek = datetime.date(year, mount, dia).strftime("%A")
                sum_total = sum_bills_to_pay(Fecha, dataJson)
                if DayWeek == 'Friday':
                    head_date += '  <div class ="col-sm-' + str(cols_xx) + '">'
                    head_date += '      <div class ="panel media pad-all bg-primary">'
                    head_date += '          <div class ="media-body">'
                    head_date += '              <p class ="mar-no" style="font-weight:bold; font-size:16pt">' + str(Fecha)  + '</p>'
                    head_date += '              <p class ="mar-no" style="font-weight:bold; font-size:12pt">' + str(sum_total) + '</p>'
                    head_date += '          </div>'
                    head_date += '      </div>'
                    head_date += '  </div>'
                    contadorCols.insert(k,str(Fecha))
                    k += 1
    head_date += '</div>'
    #here crate new cols with data

    if len(contadorCols) > 0:
        for cols in contadorCols:
            head_date += '<div class="row">'
            gap = fill_row_with_data(dataJson,cols)
            head_date += '  <div class ="col-sm-' + str(cols_xx) + '">'
            head_date += str(gap)
            head_date += '  </div>'
            head_date += '</div">'
        startDateStr = str(contadorCols[0]).split("/")
        endDateStr = str(contadorCols[-1]).split("/")
        start_date = startDateStr[2] + '-' + startDateStr[1] + '-' + startDateStr[0]
        end_date = endDateStr[2] + '-' + endDateStr[1] + '-' + endDateStr[0]
        t = total_for_week(start_date,end_date)


    ################
    #for cal_value in cal:
        #head_date += '<div class ="row text-center">'
        #for dia in cal_value:
        #    #Format here the date for dias empty
        #    if dia == 0:
        #        Fecha = '00/00/0000'
        #    else:
        #        Fecha = str(dia) + '/'  + str(mount)  + '/' +  str(year)
            #here we see if is Sat or Sun
         #   if dia > 0:
                #
        #        DayWeek = datetime.date(year, mount, dia).strftime("%A")
        #        if DayWeek == 'Saturday':
        #            vacio = 0
        #        elif DayWeek == 'Sunday':
        #            vacio = 0
        #        else:
        #            head_date += '  <div class ="col-sm-2">'
        #            head_date += '      <div class ="panel media pad-all bg-primary">'
        #            head_date += '          <div class ="media-body">'
        #            head_date += '              <p class ="mar-no">' + str(Fecha)  + '</p>'
        #            head_date += '          </div>'
        #            head_date += '      </div>'
        #            head_date += '  </div>'
        #            FilaTotalExist = 1
        #            contadorCols.insert(k,str(Fecha))
        #            k += 1
        #if FilaTotalExist > 0:
        #    head_date += '  <div class ="col-sm-2">'
        #    head_date += '      <div class ="panel media pad-all bg-primary">'
        #    head_date += '          <div class ="media-body">'
        #    head_date += '              <p class ="mar-no">Total Semanal</p>'
        #    head_date += '          </div>'
        #    head_date += '      </div>'
        #    head_date += '  </div>'
        #    FilaTotalExist = 0
        #head_date += '</div>'
        #here crate new cols with data
        #if len(contadorCols) > 0:
        #    head_date += '<div class="row">'
        #    for cols in contadorCols:
        #        gap = fill_row_with_data(dataJson,cols)
        #        head_date += '  <div class ="col-sm-2">'
        #        head_date += str(gap)
        #        head_date += '  </div>'
        #    startDateStr = str(contadorCols[0]).split("/")
        #    endDateStr = str(contadorCols[-1]).split("/")
        #    start_date = startDateStr[2] + '-' + startDateStr[1] + '-' + startDateStr[0]
        #    end_date = endDateStr[2] + '-' + endDateStr[1] + '-' + endDateStr[0]
        #    t = total_for_week(start_date,end_date)
        #    if  t == 'None':
        #        t = 0.0
        #    total_week  = babel.numbers.format_currency(str(t), 'USD', locale='en_US')
        #    head_date += '  <div class ="col-sm-2 text-center">'
        #    head_date += '      <div class ="panel media pad-all bg-primary">'
        #    head_date += '          <div class ="media-body">'
        #    head_date += '              <p class ="mar-no">' + str(total_week) + '</p>'
        #    head_date += '          </div>'
        #    head_date += '      </div>'
        #    head_date += '  </div>'
        #    head_date += '</div>'
        #    t = 0.0
        #here clean contador de cols and rows
        #contadorCols = []

    dashboard = HttpResponse()
    dashboard.write(head_date)
    return dashboard

#Here draw dahsboar in form to list tree
def load_dashboard_tree_date(request):
    time_now = datetime.datetime.now()
    year = time_now.year
    month = int(time_now.month)
    dateMonthStart = "%s-%s-01" % (year, month)
    if month > 1:
        dateMonthEnd = "%s-%s-%s" % (year, month, calendar.monthrange(year, month)[1])
    else:
        dateMonthEnd = str(year) + '-01-31'
    Tbody = ''
    Tbody += '<table id="demo-foo-pagination" class="table toggle-arrow-tiny" data-page-size="5">'
    Tbody += '	<thead>'
    Tbody += '      <tr>'
    Tbody += '          <th data-toggle="true">Proveedor</th>'
    Tbody += '          <th>Factura</th>'
    Tbody += '          <th data-hide="all">Lider</th>'
    Tbody += '          <th data-hide="all">No. Proyecto</th>'
    Tbody += '          <th data-hide="all">Contrato</th>'
    Tbody += '          <th data-hide="all">Monto</th>'
    Tbody += '          <th data-hide="all">Pagar</th>'
    Tbody += '          <th data-hide="all">Pagada</th>'
    Tbody += '          <th data-hide="all">Accion</th>'
    Tbody += '      </tr>'
    Tbody += '      <tbody>'
    Tbody += '</thead>'
    sql = 'SELECT [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Id]'  # 0
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdContrato]'  # 1
    sql += ',[SAP].[dbo].[AAAContrato].[Contrato]'  # 2
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdProveedor]'  # 3
    sql += ',[SAP].[dbo].[AAAProveedores].[Proveedor]'  # 4
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdLider]'  # 5
    sql += ',[Northwind].[dbo].[Usuarios].[Nombre]'  # 6
    sql += ',[Northwind].[dbo].[Usuarios].[Apellidos]'  # 7
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[NumProyecto]'  # 8
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Factura]'  # 9
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Monto]'  # 10
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Concepto]'  # 11
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[FechaPago]'  # 12
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Estado]'  # 13
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Iva]'  # 14
    sql += 'FROM'
    sql += '[SAP].[dbo].[AAAProveedorFacturaPoyecto],'
    sql += '[SAP].[dbo].[AAAProveedores],'
    sql += '[SAP].[dbo].[AAAContrato],'
    sql += '[Northwind].[dbo].[Usuarios]'
    sql += 'Where  ([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdProveedor = [SAP].[dbo].[AAAProveedores].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdContrato = [SAP].[dbo].[AAAContrato].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdLider = [Northwind].[dbo].[Usuarios].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago >= \'' + str(dateMonthStart) + '\' and [SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago <= \'' + str(dateMonthEnd) + '\')'

    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,
                               database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            amount = babel.numbers.format_currency(str(value[10]), 'USD', locale='en_US')
            Tbody += '<tr>'
            Tbody += '	<td>' + str(value[4]) + '</td>'
            Tbody += '	<td>' + str(value[9]) + '</td>'
            Tbody += '	<td>' + str(value[6]) + '</td>'
            Tbody += '	<td>' + str(value[8]) + '</td>'
            Tbody += '	<td>' + str(value[2]) + '</td>'
            Tbody += '	<td>' + str(amount) + '</td>'
            Tbody += '	<td>' + str(value[12].strftime("%d-%m-%Y")) + '</td>'
            Tbody += '	<td>' + str(value[13]) + '</td>'
            if str(value[13]) == 'Si':
                Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(value[0]) + ',1,' + str(value[10]) + ',' + str(value[8]) + ');"></div></div>'
            else:
                Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills" data-toggle="modal" onclick="setIdForPayStatus(' + str(value[0]) + ',\'' + str(value[9]) + '\',' + str(value[10]) + ',' + str(value[14]) + ',1)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(value[0]) + ',1,' + str(value[10]) + ',' + str(value[8]) + ');"></div></div>'
            Tbody += '</tr>'
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        Tbody = ''
    Tbody += '      </tbody>'
    Tbody += '      <tfoot>'
    Tbody += '          <tr>'
    Tbody += '              <td colspan="5">'
    Tbody += '                  <div class ="text-right"><ul class="pagination"> </ul></div>'
    Tbody += '              </td>'
    Tbody += '          </tr>'
    Tbody += '      </tfoot>'
    Tbody += '</table>'
    dashboard = HttpResponse()
    dashboard.write(Tbody)
    return dashboard

#Here draw the dashboard list this functio is for make seek
def load_dashboar_tree(request):
    Tbody =''
    Tbody += '<table id="demo-foo-pagination" class="table toggle-arrow-tiny" data-page-size="5">'
    Tbody += '	<thead>'
    Tbody += '      <tr>'
    Tbody += '          <th data-toggle="true">Proveedor</th>'
    Tbody += '          <th>Factura</th>'
    Tbody += '          <th data-hide="all">Lider</th>'
    Tbody += '          <th data-hide="all">No. Proyecto</th>'
    Tbody += '          <th data-hide="all">Contrato</th>'
    Tbody += '          <th data-hide="all">Monto</th>'
    Tbody += '          <th data-hide="all">Pagar</th>'
    Tbody += '          <th data-hide="all">Pagada</th>'
    Tbody += '          <th data-hide="all">Accion</th>'
    Tbody += '      </tr>'
    Tbody += '      <tbody>'
    Tbody += '</thead>'
    sql ='SELECT [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Id]' #0
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdContrato]' #1
    sql += ',[SAP].[dbo].[AAAContrato].[Contrato]' #2
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdProveedor]'#3
    sql += ',[SAP].[dbo].[AAAProveedores].[Proveedor]'#4
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[IdLider]'#5
    sql += ',[Northwind].[dbo].[Usuarios].[Nombre]'#6
    sql += ',[Northwind].[dbo].[Usuarios].[Apellidos]'#7
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[NumProyecto]'#8
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Factura]'#9
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Monto]'#10
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Concepto]'#11
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[FechaPago]'#12
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Estado]'#13
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Iva]'  # 14
    sql += 'FROM'
    sql += '[SAP].[dbo].[AAAProveedorFacturaPoyecto],'
    sql += '[SAP].[dbo].[AAAProveedores],'
    sql += '[SAP].[dbo].[AAAContrato],'
    sql += '[Northwind].[dbo].[Usuarios]'
    sql += 'Where  ([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdProveedor = [SAP].[dbo].[AAAProveedores].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdContrato = [SAP].[dbo].[AAAContrato].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdLider = [Northwind].[dbo].[Usuarios].Id) and'
    sql += '('
    sqlWhere = ''
    if str(request.POST['txtProviders']) != '':
        sqlWhere += ' [SAP].[dbo].[AAAProveedores].[Proveedor] like \'%' + str(request.POST['txtProviders']) + '%\' or '
    if str(request.POST['txtFactura']) != '':
        sqlWhere += ' [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Factura] like \'%' + str(request.POST['txtFactura']) + '%\' or '
    if str(request.POST['txtProyecto']) != '':
        sqlWhere += ' [SAP].[dbo].[AAAProveedorFacturaPoyecto].[NumProyecto] like \'%' + str(request.POST['txtProyecto']) + '%\' or '
    sqlWhere = sqlWhere[: -4]
    sql += sqlWhere
    sql += ')'
    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            amount = babel.numbers.format_currency(str(value[10]), 'USD', locale='en_US')
            Tbody += '<tr>'
            Tbody += '	<td>' + str(value[4]) + '</td>'
            Tbody += '	<td>' + str(value[9]) + '</td>'
            Tbody += '	<td>' + str(value[6]) + '</td>'
            Tbody += '	<td>' + str(value[8]) + '</td>'
            Tbody += '	<td>' + str(value[2]) + '</td>'
            Tbody += '	<td>' + str(amount) + '</td>'
            Tbody += '	<td>' + str(value[12].strftime("%d-%m-%Y")) +'</td>'
            Tbody += '	<td>' + str(value[13]) + '</td>'
            if str(value[13]) == 'Si':
                Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(value[0]) + ',1,' + str(value[10]) + ',' + str(value[8]) + ');"></div></div>'
            else:
                Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills" data-toggle="modal" onclick="setIdForPayStatus(' + str(value[0]) + ',\'' + str(value[9]) + '\',' + str(value[10]) + ',' + str(value[14]) + ',1)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(value[0]) + ',1,' + str(value[10]) + ',' + str(value[8]) + ');"></div></div>'
            Tbody += '</tr>'
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        Tbody = ''
    Tbody += '      </tbody>'
    Tbody += '      <tfoot>'
    Tbody += '          <tr>'
    Tbody += '              <td colspan="5">'
    Tbody += '                  <div class ="text-right"><ul class="pagination"> </ul></div>'
    Tbody += '              </td>'
    Tbody += '          </tr>'
    Tbody += '      </tfoot>'
    Tbody += '</table>'
    dashboard = HttpResponse()
    dashboard.write(Tbody)
    return dashboard



#Here calculate all sum of bill that we need pay
def sum_bills_to_pay(seekValue,dJson):
    total = 0
    for vals in dJson['Bills']:
        if vals['FechaPago'] == seekValue:
            if str(vals['Estado']) == 'No':
                total += float(vals['Monto']) + float(vals['Iva'])

    return babel.numbers.format_currency(str(total), 'USD', locale='en_US')

#Here we get balance
def get_balance(idContract):
    amount = 0
    #here get all bills with (db.T.Estado = Si)
    try:
        sql = 'SELECT [Monto],[IVA] FROM [SAP].[dbo].[AAAProveedorFacturaPoyecto] Where IdContrato = \'' + str(idContract) + '\' and Estado = \'Si\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            amount = float(value[0]) + float(value[1])
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        amount = 0
    return amount

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

