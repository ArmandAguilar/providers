from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import pypyodbc as pyodbc
import pymssql

# Create your views here.
def index(request):
    template = loader.get_template('login/login.html')
    context = {}
    return HttpResponse(template.render(context,request))

def make_login(request):
    Nick = ''
    Password= ''
    Nombre = ''
    Id = 0
    acceso = 'NO'
    if request.method == 'POST':
        Nick = request.POST['Nick']
        Password = request.POST['Password']
        #Here make login

        sql = 'SELECT [Id],[Nombre],[Apellidos],[Permisos] FROM [Northwind].[dbo].[Usuarios] Where Nombre = \'' + str(Nick) + '\' and Pwd = \'' + str(Password) + '\''
        conn = pymssql.connect(host=settings.HOSTMSSQL, user=settings.USERMSSQL, password=settings.PASSMSSQL, database=settings.DBMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        for value in cur:
            acceso = 'YES'
            Nombre = value[1]
            Id = value[0]

        conn.commit()
        conn.close()
        if acceso == 'YES':
            request.session['Nombre'] =  Nombre
            request.session ['IdUser'] = Id
        else:
            Id = 0
    return HttpResponse(Id,content_type="application/liquid; charset=utf-8")

def logout(request):
    try:
        del request.session['Nombre']
        del request.session['IdUser']
    except KeyError:
        pass
    template = loader.get_template('login/logout.html')
    context = {}
    return HttpResponse(template.render(context, request))