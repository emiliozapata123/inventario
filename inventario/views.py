from rest_framework.views import APIView
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from .models import Bodega,Producto,Inventario,Activo,Movimiento,DetalleMovimiento,ProductoActivo
from .serializers import BodegaSerializer,ProductoSerializer,ProductoWriteSerializer,InventarioSerializer,ActivoSerializer,DetalleMovimientoSerializer,ProductoActivoSerializer,ProductoActivoWriteSerializer,ActivoWriteSerializer
from rest_framework.permissions import IsAuthenticated
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
                "ubicacion":bodega.ubicacion,
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
            "ubicacion":bodega.ubicacion,
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
        
        
class InventarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            try:
                productos = Inventario.objects.filter(bodega_id=id)
                serializer = InventarioSerializer(productos, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Inventario.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        inventarios = Inventario.objects.all()
        serializer = InventarioSerializer(inventarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        bodega = request.data.get("bodega")
        productos = request.data.get("productos")
        fecha = request.data.get("fecha")
        
        movimiento = Movimiento.objects.create(
            tipo="Entrada",
            fecha=fecha,
            bodega_id=bodega
        )
               
        for producto in productos:
            stockMinimo = producto.get("stockMinimo")
            if producto["cantidad"] <= 0: 
                continue
            try:
                inventario = Inventario.objects.select_for_update().get(bodega_id=bodega,producto_id=producto["id"])
                inventario.stock+=producto["cantidad"]
                if stockMinimo is not None:
                    inventario.stockMinimo=producto["stockMinimo"]
                inventario.save()
               
                DetalleMovimiento.objects.create(
                    movimiento=movimiento,
                    producto_id=producto["id"],
                    cantidad=producto["cantidad"]
                )
            except Inventario.DoesNotExist:
                Inventario.objects.get_or_create(
                    bodega_id=bodega,
                    producto_id=producto["id"],
                    stock=producto["cantidad"],
                    stockMinimo=producto["stockMinimo"]
                )
              
                DetalleMovimiento.objects.create(
                    movimiento=movimiento,
                    producto_id=producto["id"],
                    cantidad=producto["cantidad"]
                )
                
        return Response(status=status.HTTP_201_CREATED)
    
class ProductoActivoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        productos = ProductoActivo.objects.all()
        serializer = ProductoActivoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductoActivoWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        producto = ProductoActivo.objects.get(pk=id) 
        serializer = ProductoActivoWriteSerializer(producto,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
    
    
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
    
    def post(self, request):
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
    
class ResumenActivo(APIView):
    def get(self, request):

        equipos = (
            Activo.objects
            .values("activo__tipoProducto")
            .annotate(cantidad=Count("id"))
        )
        
        return Response(equipos, status=status.HTTP_200_OK)
                
    
class ResumenInventario(APIView):
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
    
    def post(self, request):
        productos = request.data.get("productos")
        bodega = request.data.get("bodega")
        
        movimiento = Movimiento.objects.create(
            tipo="Salida",
            bodega_id=bodega
        )
        
        for producto in productos:
            if producto["cantidad"] <= 0:
                continue
            try:
                inventario = Inventario.objects.get(bodega_id=bodega,producto_id=producto["id"])
                
                inventario.stock-=producto["cantidad"]
                inventario.save()
                
                DetalleMovimiento.objects.create(
                    movimiento=movimiento,
                    producto_id=producto["id"],
                    cantidad=producto["cantidad"]
                )
            except Inventario.DoesNotExist:
                return Response({"error":"no se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_201_CREATED)

class DetalleMovimientoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        movimientos = DetalleMovimiento.objects.all()
        serializer = DetalleMovimientoSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    