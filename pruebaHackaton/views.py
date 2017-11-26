from django.shortcuts import render
from pruebaHackaton.models import Person,Usuario,TotalesView
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
            
            data=request.data
            usuario = Usuario.objects.filter(ruc=data["ruc"]).filter(username=data["username"]).filter(password=data["password"])
            dic_usuario={}
            dic={}
            if len(usuario)==0:
                dic_usuario['IsLogin']='False'
                dic_usuario['data']={}

            else:
                dic_usuario['IsLogin']='True'
                
                dic['username']=usuario[0].username
                #dic_usuario['password']=usuario[0].password
                dic['ruc']=usuario[0].ruc
                dic['nombreComercial']=usuario[0].nombreComercial
                dic_usuario['data']=dic
            r=json.dumps(dic_usuario)
            return HttpResponse(r)

#antonio
def mostrarTotales(request):
    results = TotalesView.mostrar(request.GET.get("id_cliente"))
    return HttpResponse(results)