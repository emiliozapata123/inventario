from rest_framework.views import APIView
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from .models import Bodega,Producto,Inventario,Activo,Movimiento,DetalleMovimiento
from .serializers import BodegaSerializer,ProductoSerializer,ProductoWriteSerializer,InventarioSerializer,ActivoSerializer,DetalleMovimientoSerializer,ActivoWriteSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
# Create your views here.

class BodegaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bodegas = Bodega.objects.all()
        data = []
        
        for bodega in bodegas:
            totalItems = 0
            
            for item in bodega.inventario.all():
                totalItems+=item.stock
                
            diccionario = {
                "id":bodega.id,
                "nombre":bodega.nombre,
                "totalItems":totalItems,
                "totalProductos":bodega.inventario.count()
            }
            data.append(diccionario)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BodegaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        bodega = Bodega.objects.get(pk=id)
        serializer = BodegaSerializer(bodega, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        inventario = Inventario.objects.filter(bodega_id=id).exists()

        if inventario:
            return Response(
                {"error": "la bodega tiene inventario"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bodega = Bodega.objects.get(pk=id)
            bodega.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Bodega.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class BodegaInventario(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        bodega = Bodega.objects.get(pk=id)
        
        data = {
            "id":bodega.id,
            "bodega":bodega.nombre,
            "totalProductos":bodega.inventario.count(),
            "totalItems":0,
            "productos":[],
        }
        
        for item in bodega.inventario.all():
            data["totalItems"] += item.stock
            data["productos"].append({
                "id":item.producto.id,
                "nombre":item.producto.nombre,
                "descripcion":item.producto.descripcion,
                "cantidad":item.stock
            })
        return Response(data, status=status.HTTP_200_OK) 
        
class ProductoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ProductoWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        producto = Producto.objects.get(pk=id)
        serializer = ProductoWriteSerializer(producto, data=request.data, partial=True)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request,id):
        inventario = Inventario.objects.filter(producto_id=id)

        # si existe algun registro con stock mayor a 0, no se puede eliminar
        if inventario.filter(stock__gt=0).exists():
            return Response(
                {"error": "El producto tiene stock en el inventario"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            producto = Producto.objects.get(pk=id)
            producto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class InventarioActivoView(APIView):
    def get(self, request):
        inventario = Inventario.objects.filter(producto__tipo="Activo",stock__gt=0)
        data = []
        
        for inv in inventario:
            data.append({
                "id":inv.id,
                "productoId":inv.producto.id,
                "producto":inv.producto.nombre,
                "bodega":inv.bodega.nombre,
                "bodegaId":inv.bodega.id,
                "cantidad":inv.stock,
                "descripcion":inv.producto.descripcion,
                "marca":inv.producto.marca,
                "modelo":inv.producto.modelo
            })
        return Response(data, status=status.HTTP_200_OK)
            
class InventarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            try:
                productos = Inventario.objects.filter(bodega_id=id,producto__tipo="Consumible")
                serializer = InventarioSerializer(productos, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Inventario.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        inventarios = Inventario.objects.all()
        serializer = InventarioSerializer(inventarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request):
        bodega = request.data.get("bodega")
        productos = request.data.get("productos")
        fechaEntrega = request.data.get("fechaEntrega")
        if not fechaEntrega:
            fechaEntrega = None
        
        movimiento = Movimiento.objects.create(
            tipo="Entrada",
            fechaEntrega=fechaEntrega,
            bodega_id=bodega,
            fechaMovimiento=timezone.now().date()
        )
        
        movimientoCreado = 0
               
        for producto in productos:
            stockMinimo = producto.get("stockMinimo")
            cantidad = producto.get("cantidad")
            
            if cantidad <= 0: 
                continue
            
            try:
                inventario = Inventario.objects.select_for_update().get(bodega_id=bodega,producto_id=producto["id"])
                
                inventario.stock+=cantidad
                if stockMinimo is not None:
                    inventario.stockMinimo=stockMinimo
                inventario.save()
               
                DetalleMovimiento.objects.create(
                    movimiento=movimiento,
                    producto_id=producto["id"],
                    cantidad=cantidad
                )
                
                movimientoCreado += 1
                
            except Inventario.DoesNotExist:
                Inventario.objects.create(
                    bodega_id=bodega,
                    producto_id=producto["id"],
                    stock=cantidad,
                    stockMinimo=stockMinimo
                )
              
                DetalleMovimiento.objects.create(
                    movimiento=movimiento,
                    producto_id=producto["id"],
                    cantidad=cantidad
                )
                movimientoCreado += 1
                
        if movimientoCreado == 0:
            raise Exception("No se creó ningún movimiento")
                
        return Response(status=status.HTTP_201_CREATED)
    
    
class ActivoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            producto = Activo.objects.get(pk=id)
            serializer = ActivoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            productos = Activo.objects.all()
            serializer = ActivoSerializer(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @transaction.atomic
    def post(self, request):
        invId = request.data.get("invId")
        
        inventario = Inventario.objects.get(pk=invId)
        if inventario.stock <= 0:
            return Response({"error":"inventario cantidad insuficiente"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ActivoWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        activo = Activo.objects.get(pk=id)
        serializer = ActivoWriteSerializer(activo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            
            activo = Activo.objects.get(pk=id)
            activo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Activo.DoesNotExist:
            return Response({"error":"activo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    
class ResumenInventario(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        inventario = Inventario.objects.all()
        
        totalProductos = inventario.count()
        totalItems = 0
        for item in inventario:
            totalItems += item.stock
            
        diccionario = {
            "totalProductos":totalProductos,
            "totalItems":totalItems
        }
        return Response(diccionario, status=status.HTTP_200_OK)
    
class AlertaInventario(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        inventario = Inventario.objects.all()
        
        productosFiltrados = []
        
        for producto in inventario:
            if producto.stockMinimo is not None and producto.stock < producto.stockMinimo:
                diccionario = {
                    "id":producto.id,
                    "producto":producto.producto.nombre,
                    "bodega":producto.bodega.nombre,
                    "stock":producto.stock,
                    "stockMinimo":producto.stockMinimo
                }
                productosFiltrados.append(diccionario)
        return Response(productosFiltrados, status=status.HTTP_200_OK)
            
                
class MovimientoView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        productos = request.data.get("productos")
        bodega = request.data.get("bodega")
        fechaMovimiento=request.data.get("fechaMovimiento")
        
        if not productos or not bodega:
            return Response({"error":"faltan datos"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not fechaMovimiento:
            fechaMovimiento = timezone.now().date()
            
        movimiento = Movimiento.objects.filter(
            tipo="Salida",
            bodega_id=bodega,
            fechaMovimiento=fechaMovimiento
        ).first()
        
        if not movimiento:
            movimiento = Movimiento.objects.create(
                tipo="Salida",
                bodega_id=bodega,
                fechaMovimiento=fechaMovimiento
            )
        
        movimientoCreado = 0
        for producto in productos:
            cantidad = producto.get("cantidad")
            
            if producto["cantidad"] <= 0:
                continue
            try:
                inventario = Inventario.objects.get(bodega_id=bodega,producto_id=producto["id"])
                if inventario.stock < cantidad:
                    continue
                
                if cantidad is None:
                    continue
                
                inventario.stock-=cantidad
                inventario.save()
                
                detalle = DetalleMovimiento.objects.filter(movimiento=movimiento,producto_id=producto["id"]).first()
                
                if detalle:
                    detalle.cantidad+=cantidad
                    detalle.save()
                else:
                    DetalleMovimiento.objects.create(
                        movimiento=movimiento,
                        producto_id=producto["id"],
                        cantidad=cantidad
                    )
                movimientoCreado+=1
                
            except Inventario.DoesNotExist:
                continue
            
        if movimientoCreado == 0:
            raise Exception("No se creó ningún movimiento")
        
        return Response(status=status.HTTP_201_CREATED)
    

class DetalleMovimientoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        movimientos = DetalleMovimiento.objects.all()
        serializer = DetalleMovimientoSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    