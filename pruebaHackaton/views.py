from django.shortcuts import render
from pruebaHackaton.models import Person,Usuario
from pruebaHackaton.serializers import PersonSerializer, UsuarioSerializer
from django.http import HttpResponse
from rest_framework import generics
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

#from lxml import etree

# Create your views here.
def index(request):
	return	HttpResponse('<p>hola</p>')

class PersonList(generics.ListCreateAPIView):
	queryset=Person.objects.filter(id=1)
	serializer_class=PersonSerializer



@api_view(['GET', 'POST'])
def person_list(request):
    
    if request.method == 'GET':
        
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        
        return Response(serializer.data)
    else:
        if request.method == 'POST':
            print(request.POST.get('data'))
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def usuarioValidacion(request):
    
    if request.method == 'GET':
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)      
        return Response(serializer.data)
    else:
        if request.method == 'POST':
            print("hola que kaces")
            data=request.data
            usuario = Usuario.objects.filter(ruc=data["ruc"]).filter(username=data["username"]).filter(password=data["password"])
            serializer = UsuarioSerializer(usuario, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
           
#antonio
def mostrarTotales(request):
    results = TotalesView.mostrar(request.GET.get("id_cliente"))
    dic_totales={}
    dic_totales['tfacturacion']=results[0][0]
    dic_totales['cfacturacion']=results[0][1]
    dic_totales['tpersona']=results[0][2]
    dic_totales['cpersona']=results[0][3]
    r=json.dumps(dic_totales)
    return Response(r)