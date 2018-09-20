from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('factura_proveedor/index.html')
    context = {}
    return HttpResponse(template.render(context,request))
