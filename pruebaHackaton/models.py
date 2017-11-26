from django.db import models
from django.db import connection
from django.utils import timezone
# Create your models here.
import json

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    @staticmethod  
    def search(search_string):  
        cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter  
        cur.callproc('busquedaPersona')  
        # grab the results  
        results = cur.fetchall()  
        cur.close()  
  
        # wrap the results up into Document domain objects   
        return [Person(*row) for row in results]  

class Usuario(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    ruc=models.CharField(max_length=30)
    nombreComercial=models.CharField(max_length=500,null="true")

class Direccion(models.Model):
    nombreCalle = models.CharField(max_length=200)
    distrito = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    idUsuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Cliente(models.Model):
    nodocumento = models.CharField(max_length=11)
    tipdocumento = models.CharField(max_length=10)
    direccion = models.CharField(max_length=500)
    contacto=models.CharField(max_length=50)
    nombre=models.CharField(max_length=300)

class Documento(models.Model):
    tipdocumento = models.IntegerField(default=0)
    fechaemision = models.DateTimeField()
    tipmoneda =models.CharField(max_length=50)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idCliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    total=models.FloatField()

class Detalle(models.Model):
    noorden = models.IntegerField(default=0)
    iddocumento = models.ForeignKey(Documento,on_delete=models.CASCADE)
    unidadmedida=models.CharField(max_length=50)
    cantidad=models.IntegerField(default=0)
    precio=models.IntegerField(default=0)
    producto=models.CharField(max_length=200)
    igv=models.IntegerField(default=0)

#antonio
class TotalesView(models.Model):

    def mostrar(id_usuario):
        cur=connection.cursor()
        cur.callproc('prc_totalfacturacion', id_usuario)
        
        
        dic_item={}
        dic_producto={}
        list_producto=[]
        # grab the results  
        results = cur.fetchall() 
        
        dic_item['tfacturacion']=results[0][0]
        dic_item['cfacturacion']=results[0][1]
        dic_item['tpersona']=results[0][2]
        dic_item['cpersona']=results[0][3]

        cur.close()
        cur=connection.cursor()

        cur.callproc('prc_totalproducto', id_usuario)

        results = cur.fetchall()
        for item in results:
            dic_producto['Nombre']=item[0]
            dic_producto['tventa']=int(item[1])
            dic_producto['cventa']=int(item[2])
            list_producto.append(dic_producto)

        dic_item['producto']=list_producto

        r=json.dumps(dic_item)

        cur.close()

        # wrap the results up into Document domain objects   
        return r


