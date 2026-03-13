from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Producto,Bodega,Inventario,Activo,Movimiento,DetalleMovimiento,ProductoActivo

admin.site.register(Activo)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(Inventario)
admin.site.register(Movimiento)
admin.site.register(ProductoActivo)
admin.site.register(DetalleMovimiento)


