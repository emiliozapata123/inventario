from django.urls import path,include
from .views import BodegaView,ProductoView,InventarioView,ActivoView,DetalleMovimientoView,MovimientoView,AlertaInventario,BodegaInventario,ResumenInventario,ResumenActivo,ProductoActivoView

urlpatterns = [
    #bodega 
    path('bodega/list/', BodegaView.as_view()),
    path('bodega/<int:id>/detail/',BodegaView.as_view()),
    path('bodega/form/', BodegaView.as_view()),
    path('bodega/<int:id>/update/', BodegaView.as_view()),
    path('bodega/<int:id>/delete/', BodegaView.as_view()),
    path('bodega/<int:id>/inventario/',BodegaInventario.as_view()),
    #producto
    path('producto/list/', ProductoView.as_view()),
    path('producto/form/', ProductoView.as_view()),
    path('producto/<int:id>/update/', ProductoView.as_view()),
    path('producto/<int:id>/delete/', ProductoView.as_view()),
    #inventario
    path('inventario/ingresar/producto/',InventarioView.as_view()),
    path('inventario/list/',InventarioView.as_view()),
    path('inventario/<int:id>/bodega/',InventarioView.as_view()),
    path('inventario/alert-stock/',AlertaInventario.as_view()),
    path('inventario/resumen/',ResumenInventario.as_view()),

    #producto activos
    path('activo/create/',ActivoView.as_view()),
    path('activo/list/',ActivoView.as_view()),
    path('activo/<int:id>/detail/',ActivoView.as_view()),
    path('activo/<int:id>/update/',ActivoView.as_view()),
    path('activo/resumen/',ResumenActivo.as_view()),
    path('activo/producto/create/',ProductoActivoView.as_view()),
    path('activo/producto/list/',ProductoActivoView.as_view()),
    path('activo/producto/<int:id>/update/',ProductoActivoView.as_view()),
    
    #movimiento
    path('movimiento/create/',MovimientoView.as_view()),
    path('movimiento/list/',MovimientoView.as_view()),
    path('movimiento/list/detail/',DetalleMovimientoView.as_view()),
]