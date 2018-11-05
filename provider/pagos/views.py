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
def bills_json(month,year,contable):

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
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Contable]'  # 20
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Referencia]' #21
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[ISR]' #22
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[ISRIVA]' #23
    sql += 'FROM'
    sql += '[SAP].[dbo].[AAAProveedorFacturaPoyecto],'
    sql += '[SAP].[dbo].[AAAProveedores],'
    sql += '[SAP].[dbo].[AAAContrato],'
    sql += '[Northwind].[dbo].[Usuarios]'
    sql += 'Where  ([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdProveedor = [SAP].[dbo].[AAAProveedores].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdContrato = [SAP].[dbo].[AAAContrato].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].IdLider = [Northwind].[dbo].[Usuarios].Id) and'
    sql += '([SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago >= \'' + str(dateMonthStart) + '\' and [SAP].[dbo].[AAAProveedorFacturaPoyecto].FechaPago <= \'' + str(dateMonthEnd) + '\') and [SAP].[dbo].[AAAProveedorFacturaPoyecto].Contable=\'' + str(contable) + '\''
    Ref = ''
    ISR = ''
    ISRIVA = ''
    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            if str(value[21]) == 'None':
                Ref = '0'
            else:
                Ref = str(value[21])

            if str(value[22]) == 'None':
                ISR = '0'
            else:
                ISR = str(value[22])

            if str(value[23]) == 'None':
                ISRIVA= '0'
            else:
                ISRIVA = str(value[23])

            date_small = str(value[12]).split(" ")
            ds = str(date_small[0]).split("-")
            date_format = str(int(ds[2])) + '/' + str(int(ds[1])) + '/' +  str(ds[0])
            amountBills = get_balance(value[1])
            amountBillsTotal = (float(value[15]) + float(value[16])) - float(amountBills)
            BillsJson += '{"Id":'+ str(value[0]) + ',"IdContrato":' + str(value[1]) + ',"Contrato":"' + str(value[2].strip()) + '","IdProveedor":' + str(value[3]) + ',"Proveedor":"' + str(value[4].strip()) + '","IdLider":' + str(value[5]) + ',"Nombre":"' + str(value[6]) + '","NumProyecto":' + str(value[8]) + ',"Factura":"' + str(value[9]) + '","Monto":' + str(value[10]) + ',"Concepto":"' + str(value[11].strip()) + '","FechaPago" : "' + str(date_format) + '","Estado":"' + str(value[13])+ '","Iva":' + str(value[14]) + ',"Contrato_Monto":' + str(value[14]) + ',"Contrato_IVA":' + str(value[15]) + ',"Banco":"' + str(value[17].strip()) + '","Cuenta":"' + str(value[18]) + '","Clabe":"' + str(value[19]) + '","Balance":' + str(amountBillsTotal) + ',"Contable":"' + str(value[20]) + '","Referencia":"' + str(Ref) + '","ISR":"' + str(ISR) +  '","ISRIVA":"' + str(ISRIVA) + '"},'
            Key = 1
        conn.commit()
        conn.close()
    except pymssql.Error as e:
        vars = 'SQL Error: ' + str(e)
    temp = len(BillsJson)
    BillsJson = BillsJson[:temp - 1]
    BillsJson += ']}'
    if Key > 0:
        data = json.loads(BillsJson)
        #data = BillsJson
    else:
        BillsJsonVacio = ''
        BillsJsonVacio = '{"Bills":['
        BillsJsonVacio += '{"Id":0,"IdContrato":0,"Contrato":"000","IdProveedor":0,"Proveedor":"AAA","IdLider":0,"Nombre":"AAA","NumProyecto":0,"Factura":"000","Monto":0,"Concepto":"AA","FechaPago" : "0000-00-00","Iva":0}'
        BillsJsonVacio += ']}'
        data = json.loads(BillsJsonVacio)
    return data

#here view to edit pay
def form_edit_pay(request):
    template = loader.get_template('pagos/editar_pagos.html')
    context = {}
    return HttpResponse(template.render(context, request))

#Here fill al gaps bettwen dates
def fill_row_with_data2(dJson,seekValue):
    colorbox = 'bg-gray'
    payed = 0.0
    data = ''
    #data += '<div class ="row text-center">'
    for vals in dJson['Bills']:

        if vals['FechaPago'] == seekValue:
            colorbox = 'bg-gray'
            pay = babel.numbers.format_currency(str(vals['Monto']), 'USD', locale='en_US')
            iva = babel.numbers.format_currency(str(vals['Iva']), 'USD', locale='en_US')
            btwiva = (float(vals['Monto']) + float(vals['Iva'])) - (float(vals['ISR']) + float(vals['ISRIVA']))
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
            if str(vals['Estado']) == 'Si' and str(vals['Factura']) == 'Provisionar':
                colorbox = 'bg-mint'
                payed = bill_whit_iva
             #Here print the data
            data += '  <div class ="row text-left text-bold"><div class ="col-sm-12">'
            data += '      <div class ="panel media pad-all ' + str(colorbox) + '">'
            data += '          <div class ="media-body">'
            data += '              <p class ="mar-no" data-target="#modal-rank" data-toggle="modal">Lider:' + str(vals['Nombre']) + '</p>'
            data += '              <p class ="mar-no">NoProyecto:' + str(vals['NumProyecto']) + '</p>'
            data += '              <p class ="mar-no">' + str(vals['Proveedor']) + '</p>'
            data += '              <p class ="mar-no">Contrato:' + str(contract_whit_iva) + '</p>'
            data += '              <p class ="mar-no">Factura:' + str(vals['Factura']) + '</p>'
            if str(vals['Referencia']) != '0':
                data += '        <p class ="mar-no">Ref:' + str(vals['Referencia']) + '</p>'
            data += '              <p class ="mar-no">Monto:' + str(pay) + '</p>'
            data += '              <p class ="mar-no">Iva:' + str(iva) + '</p>'

            if float(vals['ISR']) > 0:
                isr = babel.numbers.format_currency(str(vals['ISR']), 'USD', locale='en_US')
                data += '              <p class ="mar-no">ISR:' + str(isr) + '</p>'
            if float(vals['ISRIVA']) > 0:
                isriva = babel.numbers.format_currency(str(vals['ISRIVA']), 'USD', locale='en_US')
                data += '              <p class ="mar-no">ISRIVA:' + str(isriva) + '</p>'

            data += '              <p class ="mar-no">Pagado:' + str(payed) + '</p>'
            data += '              <p class ="mar-no">Saldo:' + str(balance) + '</p>'

            data += '            <p class ="mar-no">Total:' + str(bill_whit_iva) + '</p>'
            data += '            <p class ="mar-no">&nbsp;</p>'

            if str(vals['Contable']) == 'Si':
                if str(vals['Estado']) == 'Si':
                    data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\''  + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk('+ str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-thumbs-o-up fa-lg" data-target="#modal-like" data-toggle="modal" onclick="set_valProveederReview(' + str(vals['NumProyecto']) + ',' + str(vals['IdProveedor']) + ')"></div></div>'
                else:
                    data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\'' + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk(' + str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(vals['Id']) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills" data-toggle="modal" onclick="setIdForPayStatus(' + str(vals['Id']) + ',\'' + str(vals['Factura']) + '\',' + str(vals['Monto']) + ',' + str(vals['Iva']) + ',0)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(vals['Id']) + ',1,' + str(float(vals['Monto'])  + float(vals['Iva'])) + ',' + str(vals['NumProyecto']) + ');"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-thumbs-o-up fa-lg"  data-target="#modal-like" data-toggle="modal" onclick="set_valProveederReview(' + str(vals['NumProyecto']) + ',' + str(vals['IdProveedor']) + ')"></div></div>'
            else:
                if str(vals['Estado']) == 'Si':
                    data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\''  + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk('+ str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-thumbs-o-up fa-lg" data-target="#modal-like" data-toggle="modal" onclick="set_valProveederReview(' + str(vals['NumProyecto']) + ',' + str(vals['IdProveedor']) + ')"></div></div>'
                else:
                    data += '     <div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(vals['Id']) + ',\'' + str(vals['FechaPago']) + '\',0);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk(' + str(vals['IdProveedor']) + ',\'' + str(vals['Banco']) + '\',\'' + str(vals['Cuenta']) + '\',\'' + str(vals['Clabe']) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(vals['Id']) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills-uncontable" data-toggle="modal" onclick="setIdForPayStatus_uncontable(' + str(vals['Id']) + ',\'' + str(vals['Factura']) + '\',' + str(vals['Monto']) + ',' + str(vals['Iva']) + ',0)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel-uncontable" data-toggle="modal" onclick="setIdForCancel_uncontable(' + str(vals['Id']) + ',1,' + str(float(vals['Monto']) + float(vals['Iva'])) + ',' + str(vals['NumProyecto']) + ');"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-thumbs-o-up fa-lg" data-target="#modal-like" data-toggle="modal" onclick="set_valProveederReview(' + str(vals['NumProyecto']) + ',' + str(vals['IdProveedor']) + ')"></div></div>'
            data += '          </div>'
            data += '      </div>'
            data += '  </div></div>'
    #data += '</div>'
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
            if str(request.POST['txtuncontable']) == 'Si':
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

        try:

            if str(request.POST['txtuncontable']) == 'Si':
                if int(request.POST['txtNumProy'])  > 100:
                    decrees_charge(request.POST['txtNumProy'], request.POST['txtMonto'])
            else:
                val = 0
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
    sql += ', [SAP].[dbo].[AAAProveedorFacturaPoyecto].[Contable]'  # 14
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Referencia]'  # 15
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[ISR]'  # 16
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[ISRIVA]'  # 17
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
                'contable':value[14],
                'ref':value[15],
                'isr':value[16],
                'isriva':value[17]
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
    apellidos = ''
    if request.method == 'POST':
        try:
            Sql = 'Select Id,Nombre,Apellidos From [Northwind].[dbo].[Usuarios] Where (CobranzaPerfil =\'Admin\' or CobranzaPerfil=\'User\') and (Departamento <> \'Baja\') order by Nombre'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQLNORTHWIND)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                apellidos = value[2].decode("iso-8859-1")
                if value[0] == str(request.POST['txtidLeader']):
                    data_text += '<option value="' + str(value[0]) + '" selected>' + str(value[1]) + ' ' + str(apellidos.encode("iso-8859-1")) + '</option>'
                else:
                    data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + ' ' + str(apellidos.encode("iso-8859-1")) + '</option>'
            conn.commit()
            conn.close()
        except ValueError:
            data_text = ValueError
        cbo_data = HttpResponse()
        cbo_data.write(data_text)
    return cbo_data
#Here seek contrato
def seek_contract(request):
    data_text = ''
    amount = 0
    total = 0
    if request.method == 'POST':
        try:
            Sql = 'SELECT [Id],[Contrato],[Monto],[Iva] FROM [SAP].[dbo].[AAAContrato] Where [IdProveedor]=\'' + str(request.POST['txtIdProvider']) + '\''
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(Sql)
            for value in cur:
                total = float(value[2]) + float(value[3])
                amount = babel.numbers.format_currency(str(total), 'USD', locale='en_US')
                if str(value[0]) == str(request.POST['txtIdContract']):
                    data_text += '<option value="' + str(value[0]) + '" selected>' + str(value[1]) + ' x ' + str(amount) + '</option>'
                else:
                    data_text += '<option value="' + str(value[0]) + '">' + str(value[1]) + ' x ' + str(amount) + '</option>'

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
            if 'txtISR' not in request.POST:
                sql += ', [ISR] = \'0\''
            else:
                sql += ', [ISR] = \'' + str(request.POST['txtISR']) + '\''
            if 'txtISRIVA' not in request.POST:
                sql += ', [ISRIVA] = \'0\''
            else:
                sql += ', [ISRIVA] = \'' + str(request.POST['txtISRIVA']) + '\''

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
    contable = ''
    if request.method == 'POST':
        mount = int(request.POST['CboMes'])
        year = int(request.POST['txtYear'])
        contable = str(request.POST['txtContable'])
    else:
        #mount = 7
        #year = 2018
        time_now = datetime.datetime.now()
        year = time_now.year
        mount = int(time_now.month)
        contable = 'Si'
    Fecha = '00/00/0000'

    contadorCols = []
    k = 0
    cal = calendar.monthcalendar(year, mount)
    dataJson = bills_json(mount, year, contable)
    head_date += '<div class ="row text-center">'
    cols_x = 0
    cols_xx = 3
    off_set = ''
    for cal_value in cal:
        for dia in cal_value:
            if dia > 0:
                DayWeek = datetime.date(year, mount, dia).strftime("%A")
                if DayWeek == 'Friday':
                    cols_x += 1
    if cols_x > 4:
        cols_xx = 2
        off_set = 'col-sm-offset-1'

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
                #sum_total = 0
                if DayWeek == 'Friday':
                    head_date += '  <div class ="col-sm-' + str(cols_xx) +  ' '  + str(off_set) + '">'
                    head_date += '      <div class="row">'
                    head_date += '          <div class ="panel media pad-all bg-primary">'
                    head_date += '              <div class ="media-body">'
                    head_date += '                  <p class ="mar-no" style="font-weight:bold; font-size:16pt">' + str(Fecha)  + '</p>'
                    head_date += '                  <p class ="mar-no" style="font-weight:bold; font-size:12pt">' + str(sum_total) + '</p>'
                    head_date += '              </div>'
                    head_date += '          </div>'
                    head_date += '      </div>'
                    off_set = ''
                    gap = fill_row_with_data2(dataJson,Fecha)
                    #gap = ''
                    head_date += str(gap)
                    head_date += '  </div>'
                    contadorCols.insert(k,str(Fecha))
                    k += 1
    head_date += '</div>'

    dashboard = HttpResponse()
    dashboard.write(head_date)
    return dashboard

#Here's the fucntion that you need change###### <-------
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
    Tbody += '          <th data-hide="all">Proveedor</th>'
    Tbody += '          <th data-hide="all">Contrato</th>'
    Tbody += '          <th data-hide="all">Factura</th>'
    Tbody += '          <th data-hide="all">Monto</th>'
    Tbody += '          <th data-hide="all">IVA</th>'
    Tbody += '          <th data-hide="all">Total</th>'
    Tbody += '          <th data-hide="all">Pagado</th>'
    Tbody += '          <th data-hide="all">Saldo</th>'
    Tbody += '          <th data-hide="all">Banco</th>'
    Tbody += '          <th data-hide="all">Cuenta</th>'
    Tbody += '          <th data-hide="all">Clabe</th>'
    Tbody += '          <th data-hide="all">Referencia</th>'
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
    sql += ',[SAP].[dbo].[AAAContrato].[Monto]'  # 15
    sql += ',[SAP].[dbo].[AAAContrato].[Iva]'  # 16
    sql += ',[SAP].[dbo].[AAAProveedores].[Banco]'  # 17
    sql += ',[SAP].[dbo].[AAAProveedores].[Cuenta]'  # 18
    sql += ',[SAP].[dbo].[AAAProveedores].[Clabe]'  # 19
    sql += ',[SAP].[dbo].[AAAProveedorFacturaPoyecto].[Contable]'  # 20
    sql += ',[SAP].[dbo].[AAAProveedores].[Referencia]'  # 21
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
    if str(request.POST['txtFechaPago']) != '':
        sqlWhere += ' [SAP].[dbo].[AAAProveedorFacturaPoyecto].[FechaPago] = \'' + str(request.POST['txtFechaPago']) + '\' or '
    sqlWhere = sqlWhere[: -4]
    sql += sqlWhere
    sql += ') and [SAP].[dbo].[AAAProveedorFacturaPoyecto].Contable = \'' + str(request.POST['txtContableNodo']) + '\''


    try:
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            payed = '$0.0'
            #Bills
            amount = babel.numbers.format_currency(str(value[10]), 'USD', locale='en_US')
            iva = babel.numbers.format_currency(str(float(value[14])), 'USD', locale='en_US')
            total_bill = babel.numbers.format_currency(str(float(value[10]) + float(value[14])), 'USD', locale='en_US')
            #Contract
            contract = babel.numbers.format_currency(str(float(value[15]) + float(value[16])), 'USD', locale='en_US')
            #balance
            amountBills = get_balance(value[1])
            amountBillsTotal = (float(value[15]) + float(value[16])) - float(amountBills)
            balance = babel.numbers.format_currency(str(amountBillsTotal), 'USD', locale='en_US')

            if str(value[13]) == 'Si' and float(value[14])  > 0:
                payed = total_bill
            if str(value[13]) == 'Si' and float(value[14]) == 0:
                payed = total_bill

            Tbody += '<tr>'
            Tbody += '	<td>' + str(value[4]) + '</td>'
            Tbody += '	<td>' + str(value[9]) + '</td>'
            Tbody += '	<td>' + str(value[6]) + '</td>'
            Tbody += '	<td>' + str(value[8]) + '</td>'
            Tbody += '	<td>' + str(value[4]) + '</td>'
            Tbody += '	<td>' + str(contract) + '</td>'
            Tbody += '	<td>' + str(value[9]) + '</td>'
            Tbody += '	<td>' + str(amount) + '</td>'
            Tbody += '	<td>' + str(iva) + '</td>'
            Tbody += '	<td>' + str(total_bill) + '</td>'
            Tbody += '	<td>' + str(payed) + '</td>'
            Tbody += '	<td>' + str(balance) + '</td>'
            Tbody += '	<td>' + str(value[17]) + '</td>'
            Tbody += '	<td>' + str(value[18]) + '</td>'
            Tbody += '	<td>' + str(value[19]) + '</td>'
            Tbody += '	<td>' + str(value[21]) + '</td>'

            if str(value[13]) == 'Si':
                Tbody += ' <td><div class ="text-center" style="cursor:pointer"><div class ="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\''  + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class ="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk('+ str(value[3]) + ',\'' + str(value[17]) + '\',\'' + str(value[18]) + '\',\'' + str(value[19]) + '\'' + ')"></div></div>'
            else:
                if str(value[20]) == 'Si':
                    Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk(' + str(value[3]) + ',\'' + str(value[17]) + '\',\'' + str(value[18]) + '\',\'' + str(value[19]) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills" data-toggle="modal" onclick="setIdForPayStatus(' + str(value[0]) + ',\'' + str(value[9]) + '\',' + str(value[10]) + ',' + str(value[14]) + ',1)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel" data-toggle="modal" onclick="setIdForCancel(' + str(value[0]) + ',1,' + str(float(value[10]) + float(value[14])) + ',' + str(value[8]) + ');"></div></div>'
                else:
                    Tbody += '  <td><div class ="text-center" style="cursor:pointer"><div class="fa fa-calendar fa-lg" data-target="#modal-calendar" data-toggle="modal" onclick="setIdForDate(' + str(value[0]) + ',\'' + str(value[12]) + '\',1);"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-bank" data-target="#modal-banco" data-toggle="modal" onclick="set_idProviders_bnk(' + str(value[3]) + ',\'' + str(value[17]) + '\',\'' + str(value[18]) + '\',\'' + str(value[19]) + '\'' + ')"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-edit fa-lg" onclick=link_go(\'/pagos/form_edit/bill/' + str(value[0]) + '\')></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-check fa-lg" data-target="#modal-bills-uncontable" data-toggle="modal" onclick="setIdForPayStatus_uncontable(' + str(value[0]) + ',\'' + str(value[9]) + '\',' + str(value[10]) + ',' + str(value[14]) + ',1)"></div>&nbsp;&nbsp;&nbsp;<div class="fa fa-close fa-lg" data-target="#modal-cancel-uncontable" data-toggle="modal" onclick="setIdForCancel_uncontable(' + str(value[0]) + ',1,' + str(float(value[10]) + float(value[14])) + ',' + str(value[8]) + ');"></div></div>'

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
                total += (float(vals['Monto']) + float(vals['Iva']))  - (float(vals['ISR']) + float(vals['ISRIVA']))

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

#Here function for califications
def review_add(request):
    status = 0
    if request.method == 'POST':
        try:
            if request.POST['txtComentario'] == '':
                val = 0
            else:
                SqlObservaciones = 'INSERT INTO [SAP].[dbo].[AAAProveedoresObservaciones] VALUES (\'' + str(request.POST['IdProyectoReview']) + '\',\'' + str(request.POST['IdProveedorReview']) + '\',\'' + str(request.POST['txtComentario']) + '\',\'' + str(request.POST['IdUserReview']) + '\')'
                conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
                cur = conn.cursor()
                cur.execute(SqlObservaciones)
                conn.commit()
                conn.close()

            B = ''
            R = ''
            M = ''
            if (request.POST['CboCalidad'] == 'B'):
                B = 'B'
            elif request.POST['CboCalidad'] == 'R':
                R = 'R'
            elif request.POST['CboCalidad'] == 'M':
                M = 'M'
            SqlCalidadTrabajo = 'INSERT INTO [SAP].[dbo].[AAAProveedorCalidadTrabajo] VALUES (\'' + str(request.POST['IdProyectoReview']) + '\',\'' + str(request.POST['IdProveedorReview']) + '\',\'' + str(request.POST['IdUserReview']) + '\',\'' + str(B) + '\',\'' + str(R) + '\',\'' + str(M) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(SqlCalidadTrabajo)
            conn.commit()
            conn.close()

            Rapida = ''
            Media = ''
            Nula = ''
            if (request.POST['CboEntrega'] == 'R'):
                Rapida = 'R'
            elif request.POST['CboEntrega'] == 'M':
                Media = 'M'
            elif request.POST['CboEntrega'] == 'N':
                Nula = 'N'

            SqlEntregaTrabajo = 'INSERT INTO [SAP].[dbo].[AAAProveedorEntregaDeTrabajo] VALUES (\'' + str(request.POST['IdProyectoReview']) + '\',\'' + str(request.POST['IdProveedorReview']) + '\',\'' + str(request.POST['IdUserReview']) + '\',\'' + str(Rapida) + '\',\'' + str(Media) + '\',\'' + str(Nula) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(SqlEntregaTrabajo)
            conn.commit()
            conn.close()

            Alto = ''
            Aceptable = ''
            Bajo = ''
            if (request.POST['CboCalificacion'] == 'A'):
                Alto = 'A'
            elif request.POST['CboCalificacion'] == 'AC':
                Aceptable = 'AC'
            elif request.POST['CboCalificacion'] == 'B':
                Bajo = 'B'

            SqlCalificacion = 'INSERT INTO [SAP].[dbo].[AAAProveedorCalificacion] VALUES (\'' + str(request.POST['IdProyectoReview']) + '\',\'' + str(request.POST['IdProveedorReview']) + '\',\'' + str(request.POST['IdUserReview']) + '\',\'' + str(Alto) + '\',\'' + str(Aceptable) + '\',\'' + str(Bajo) + '\')'
            conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL,database=settings.DBMSSQL)
            cur = conn.cursor()
            cur.execute(SqlCalificacion)
            conn.commit()
            conn.close()

            status = 1
        except pymssql.Error as e:
            status = 0

        return HttpResponse(status, content_type="application/liquid charset=utf-8;")