from django.urls import path
from . import views

urlpatterns = [
    # ======= INICIO =======
    path('', views.inicio_jugueteria, name='inicio'),

    # ======= SUCURSALES =======
    path('sucursales/', views.ver_sucursales, name='ver_sucursales'),
    path('sucursales/agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('sucursales/actualizar/<int:id>/', views.actualizar_sucursal, name='actualizar_sucursal'),
    path('sucursales/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_sucursal, name='realizar_actualizacion_sucursal'),
    path('sucursales/borrar/<int:id>/', views.borrar_sucursal, name='borrar_sucursal'),

    # ======= EMPLEADOS =======
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),


    # ===== CLIENTES =====
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('clientes/borrar/<int:id>/', views.borrar_cliente, name='borrar_cliente'),

        # CATEGORIAS
    path('categorias/', views.ver_categorias, name='ver_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/actualizar/<int:id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categorias/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_categoria, name='realizar_actualizacion_categoria'),
    path('categorias/borrar/<int:id>/', views.borrar_categoria, name='borrar_categoria'),

    # PRODUCTOS
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/realizar_actualizacion/<int:id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('productos/borrar/<int:id>/', views.borrar_producto, name='borrar_producto'),

]