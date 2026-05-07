from django.db import models
from accounts.models import Profile
# Create your models here.

class Bodega(models.Model):
    nombre=models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    TIPO_PRODUCTO=(
        ("Activo","Activo"),
        ("Consumible","Consumible"),
    )
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(blank=True,null=True)
    tipo=models.CharField(max_length=20, choices=TIPO_PRODUCTO, default="Consumible")
    marca=models.CharField(max_length=100, blank=True, null=True)
    modelo=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"
    
class Activo(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    numeroInventario=models.CharField(max_length=100, unique=True, blank=True,null=True)
    numeroSerie=models.CharField(max_length=100, blank=True, null=True)
    ubicacion=models.CharField(max_length=100,blank=True,null=True)
    usuario=models.CharField(max_length=100,blank=True,null=True)
    cargo=models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.numeroInventario}"
    
class Inventario(models.Model):
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    bodega=models.ForeignKey(Bodega,on_delete=models.CASCADE, related_name="inventario")
    stock=models.PositiveIntegerField(default=0)
    stockMinimo=models.PositiveIntegerField(blank=True,null=True,default=0)
    
    def __str__(self):
        return f"{self.producto.nombre}-{self.bodega}-{self.stock}"

class Movimiento(models.Model):
    TIPO_MOVIMIENTO = (
        ("Entrada","Entrada"),
        ("Salida","Salida"),
    )
    
    tipo=models.CharField(max_length=100)
    usuario=models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    fechaEntrega=models.DateField(blank=True, null=True)
    fechaMovimiento=models.DateField()
    bodega=models.ForeignKey(Bodega,on_delete=models.CASCADE)

class DetalleMovimiento(models.Model):
    movimiento=models.ForeignKey(Movimiento,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.PositiveIntegerField()