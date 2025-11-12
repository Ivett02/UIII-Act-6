from django.contrib import admin
from django.utils.html import format_html
from .models import Sucursal, Cliente, Empleado, Categoria, Producto

# ==========================
# ADMIN: Sucursal
# ==========================
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'estado', 'thumbnail')
    readonly_fields = ('thumbnail',)
    search_fields = ('nombre', 'ciudad', 'estado')
    list_filter = ('estado', 'ciudad')

    def thumbnail(self, obj):
        if hasattr(obj, 'imagen') and obj.imagen:
            return format_html('<img src="{}" style="max-width:120px;"/>', obj.imagen.url)
        return '-'
    thumbnail.short_description = 'Imagen'


# ==========================
# ADMIN: Cliente
# ==========================
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'telefono', 'email', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'telefono', 'email')
    list_filter = ('id_sucursal',)


# ==========================
# ADMIN: Empleado
# ==========================
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'puesto', 'salario', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'puesto')
    list_filter = ('id_sucursal', 'puesto')


# ==========================
# ADMIN: Categoria
# ==========================
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado', 'material', 'fecha_creacion')
    list_filter = ('estado', 'material')
    search_fields = ('nombre', 'material')
    readonly_fields = ('fecha_creacion',)


# ==========================
# ADMIN: Producto
# ==========================
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'stock', 'precio', 'get_categoria')
    list_filter = ('id_categoria',)
    search_fields = ('nombre',)
    def get_categoria(self, obj):
        return obj.id_categoria.nombre if obj.id_categoria else '-'
    get_categoria.short_description = 'Categoría'


# ==========================
# Registro en el panel
# ==========================
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
