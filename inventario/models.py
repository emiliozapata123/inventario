from django.db import models

# Create your models here.

class Bodega(models.Model):
    nombre=models.CharField(max_length=100)
    ubicacion=models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"
    
class ProductoActivo(models.Model):
    tipoProducto=models.CharField(max_length=100,blank=True,null=True)
    descripcion=models.TextField(blank=True,null=True)
    marca=models.CharField(max_length=100, blank=True,null=True)
    modelo=models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return f"{self.tipoProducto} - {self.descripcion}"
    
class Activo(models.Model):
    activo=models.ForeignKey(ProductoActivo,on_delete=models.CASCADE)
    numeroInventario=models.CharField(max_length=100, unique=True, blank=True,null=True)
    numeroSerie=models.CharField(max_length=100, blank=True, null=True)
    fechaEntrega=models.DateField()
    ubicacion=models.CharField(max_length=100,blank=True,null=True)
    usuario=models.CharField(max_length=100,blank=True,null=True)
    cargo=models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return f"{self.activo.tipoProducto} - {self.numeroInventario}"
    
    
class Inventario(models.Model):
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    bodega=models.ForeignKey(Bodega,on_delete=models.CASCADE, related_name="inventario")
    stock=models.PositiveIntegerField(default=0)
    stockMinimo=models.PositiveIntegerField(blank=True,null=True,default=0)
    
    def __str__(self):
        return f"{self.producto}-{self.bodega}-{self.stock}"

class Movimiento(models.Model):
    TIPO_MOVIMIENTO = (
        ("Entrada","Entrada"),
        ("Salida","Salida"),
    )
    
    tipo=models.CharField(max_length=100)
    fecha=models.DateField(auto_now_add=True)
    bodega=models.ForeignKey(Bodega,on_delete=models.CASCADE)

class DetalleMovimiento(models.Model):
    movimiento=models.ForeignKey(Movimiento,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.PositiveIntegerField()