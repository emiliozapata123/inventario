from rest_framework import serializers
from accounts.serializers import ProfileSerializer
from .models import Producto,Bodega,Inventario,Activo,Movimiento,DetalleMovimiento

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

class ActivoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model=Activo
        fields="__all__"
    
class ActivoWriteSerializer(serializers.ModelSerializer):
    numeroInventario = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    class Meta:
        model=Activo
        fields="__all__"
    
    def validate_numeroInventario(self, value):
        if value == "":
            return None
        return value
    
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
    usuario = ProfileSerializer()
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
        