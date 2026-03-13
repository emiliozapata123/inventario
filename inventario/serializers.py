from rest_framework import serializers
from .models import Producto,Bodega,Inventario,Activo,Movimiento,DetalleMovimiento,ProductoActivo
from accounts.serializers import ProfileSerializer

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bodega
        fields="__all__"
        
class ProductoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields="__all__"
        
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields="__all__"
        
        
        

class ProductoActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductoActivo
        fields="__all__"
        
class ProductoActivoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductoActivo
        fields="__all__"
        
class ActivoSerializer(serializers.ModelSerializer):
    activo = ProductoActivoSerializer()
    class Meta:
        model=Activo
        fields="__all__"
    
class ActivoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Activo
        fields="__all__"
    
    
class InventarioSerializer(serializers.ModelSerializer):
    bodega=BodegaSerializer()
    producto=ProductoSerializer()
    class Meta:
        model=Inventario
        fields="__all__"
    
class InventarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inventario
        fields="__all__"

class MovimientoSerializer(serializers.ModelSerializer):
    bodega = BodegaSerializer()
    class Meta:
        model=Movimiento
        fields="__all__"
        
class MovimientoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movimiento
        fields="__all__"
        
class DetalleMovimientoSerializer(serializers.ModelSerializer):
    movimiento = MovimientoSerializer()
    producto = ProductoSerializer()
    class Meta:
        model=DetalleMovimiento
        fields="__all__"
        