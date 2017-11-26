from django.db import models
from django.db import connection
from django.utils import timezone
# Create your models here.

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