from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Sucursal, Empleado, Cliente, Categoria, Producto

# =================================
# INICIO
# =================================
def inicio_jugueteria(request):
    contexto = {'fecha': timezone.now()}
    return render(request, 'inicio.html', contexto)


# =================================
# SUCURSALES (CRUD)
# =================================
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        direccion = request.POST.get('direccion', '')
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        telefono = request.POST.get('telefono', '')
        codigo_postal = request.POST.get('codigo_postal', '')
        email = request.POST.get('email', '')

        # Crear la sucursal primero
        sucursal = Sucursal.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            estado=estado,
            telefono=telefono,
            codigo_postal=codigo_postal,
            email=email
        )

        # Guardar imagen si se subió (manejo seguro)
        if request.FILES.get('imagen'):
            try:
                sucursal.imagen = request.FILES['imagen']
                sucursal.save()
            except Exception as e:
                # imprimir en consola para depuración en desarrollo
                print('Error guardando imagen de sucursal:', e)

        return redirect('ver_sucursales')

    return render(request, 'sucursal/agregar_sucursal.html')


def ver_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('id')
    return render(request, 'sucursal/ver_sucursales.html', {'sucursales': sucursales})


def actualizar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': sucursal})


def realizar_actualizacion_sucursal(request, id):
    if request.method == 'POST':
        sucursal = get_object_or_404(Sucursal, id=id)
        sucursal.nombre = request.POST.get('nombre', sucursal.nombre)
        sucursal.direccion = request.POST.get('direccion', sucursal.direccion)
        sucursal.ciudad = request.POST.get('ciudad', sucursal.ciudad)
        sucursal.estado = request.POST.get('estado', sucursal.estado)
        sucursal.telefono = request.POST.get('telefono', sucursal.telefono)
        sucursal.codigo_postal = request.POST.get('codigo_postal', sucursal.codigo_postal)
        sucursal.email = request.POST.get('email', sucursal.email)

        if request.FILES.get('imagen'):
            try:
                sucursal.imagen = request.FILES['imagen']
            except Exception as e:
                print('Error al actualizar imagen de sucursal:', e)

        sucursal.save()
        return redirect('ver_sucursales')

    return redirect('actualizar_sucursal', id=id)


def borrar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('ver_sucursales')
    return render(request, 'sucursal/borrar_sucursal.html', {'sucursal': sucursal})


# =================================
# EMPLEADOS (CRUD)
# =================================
def ver_empleados(request):
    empleados = Empleado.objects.select_related('id_sucursal').all().order_by('id')
    return render(request, 'empleado/ver_empleados.html', {'empleados': empleados})


def agregar_empleado(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')

        # edad -> int o None
        edad_raw = request.POST.get('edad')
        try:
            edad = int(edad_raw) if edad_raw not in (None, '') else None
        except (ValueError, TypeError):
            edad = None

        direccion = request.POST.get('direccion', '')
        puesto = request.POST.get('puesto', '')

        # salario -> Decimal o None
        salario_raw = request.POST.get('salario')
        try:
            salario = Decimal(salario_raw) if salario_raw not in (None, '') else None
        except (InvalidOperation, TypeError):
            salario = None

        id_sucursal = request.POST.get('id_sucursal')  # puede venir vacío

        empleado = Empleado.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            direccion=direccion,
            puesto=puesto,
            salario=salario,
            id_sucursal=Sucursal.objects.get(pk=id_sucursal) if id_sucursal else None
        )
        return redirect('ver_empleados')

    return render(request, 'empleado/agregar_empleado.html', {'sucursales': sucursales})


def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado, 'sucursales': sucursales})


def realizar_actualizacion_empleado(request, id):
    if request.method == 'POST':
        empleado = get_object_or_404(Empleado, id=id)
        empleado.nombre = request.POST.get('nombre', empleado.nombre)
        empleado.apellido = request.POST.get('apellido', empleado.apellido)

        edad_raw = request.POST.get('edad')
        try:
            empleado.edad = int(edad_raw) if edad_raw not in (None, '') else None
        except (ValueError, TypeError):
            pass

        empleado.direccion = request.POST.get('direccion', empleado.direccion)
        empleado.puesto = request.POST.get('puesto', empleado.puesto)

        salario_raw = request.POST.get('salario')
        try:
            empleado.salario = Decimal(salario_raw) if salario_raw not in (None, '') else empleado.salario
        except (InvalidOperation, TypeError):
            pass

        id_sucursal = request.POST.get('id_sucursal')
        if id_sucursal:
            empleado.id_sucursal = Sucursal.objects.get(pk=id_sucursal)
        else:
            empleado.id_sucursal = None

        empleado.save()
        return redirect('ver_empleados')

    return redirect('ver_empleados')


def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleado/borrar_empleado.html', {'empleado': empleado})


# =================================
# CLIENTES (CRUD)
# =================================
def ver_clientes(request):
    clientes = Cliente.objects.select_related('id_sucursal').all().order_by('id')
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})


def agregar_cliente(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')

        edad_raw = request.POST.get('edad')
        try:
            edad = int(edad_raw) if edad_raw not in (None, '') else None
        except (ValueError, TypeError):
            edad = None

        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        id_sucursal = request.POST.get('id_sucursal')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            direccion=direccion,
            telefono=telefono,
            email=email,
            id_sucursal=Sucursal.objects.get(pk=id_sucursal) if id_sucursal else None
        )
        return redirect('ver_clientes')

    return render(request, 'cliente/agregar_cliente.html', {'sucursales': sucursales})


def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente, 'sucursales': sucursales})


def realizar_actualizacion_cliente(request, id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.apellido = request.POST.get('apellido', cliente.apellido)

        edad_raw = request.POST.get('edad')
        try:
            cliente.edad = int(edad_raw) if edad_raw not in (None, '') else cliente.edad
        except (ValueError, TypeError):
            pass

        cliente.direccion = request.POST.get('direccion', cliente.direccion)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.email = request.POST.get('email', cliente.email)

        id_sucursal = request.POST.get('id_sucursal')
        if id_sucursal:
            cliente.id_sucursal = Sucursal.objects.get(pk=id_sucursal)
        else:
            cliente.id_sucursal = None

        cliente.save()
        return redirect('ver_clientes')

    return redirect('ver_clientes')


def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})


# =========================
# CATEGORIAS (CRUD)
# =========================
def ver_categorias(request):
    categorias = Categoria.objects.all().order_by('id')
    return render(request, 'categoria/ver_categorias.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        descripcion = request.POST.get('descripcion', '')
        estado = True if request.POST.get('estado') == 'on' else False
        material = request.POST.get('material', '')
        Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            material=material
        )
        return redirect('ver_categorias')
    return render(request, 'categoria/agregar_categoria.html')

def actualizar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    return render(request, 'categoria/actualizar_categoria.html', {'categoria': categoria})

def realizar_actualizacion_categoria(request, id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id=id)
        categoria.nombre = request.POST.get('nombre', categoria.nombre)
        categoria.descripcion = request.POST.get('descripcion', categoria.descripcion)
        categoria.material = request.POST.get('material', categoria.material)
        categoria.estado = True if request.POST.get('estado') == 'on' else False
        categoria.save()
        return redirect('ver_categorias')
    return redirect('ver_categorias')

def borrar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('ver_categorias')
    return render(request, 'categoria/borrar_categoria.html', {'categoria': categoria})


# =========================
# PRODUCTOS (CRUD)
# =========================
def ver_productos(request):
    productos = Producto.objects.select_related('id_categoria').all().order_by('id')
    return render(request, 'producto/ver_productos.html', {'productos': productos})

def agregar_producto(request):
    categorias = Categoria.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        stock_raw = request.POST.get('stock') or 0
        try:
            stock = int(stock_raw)
        except (ValueError, TypeError):
            stock = 0
        descripcion = request.POST.get('descripcion', '')
        precio_raw = request.POST.get('precio') or '0'
        try:
            precio = Decimal(precio_raw)
        except (InvalidOperation, TypeError):
            precio = Decimal('0')
        id_categoria = request.POST.get('id_categoria')

        Producto.objects.create(
            nombre=nombre,
            stock=stock,
            descripcion=descripcion,
            precio=precio,
            id_categoria=Categoria.objects.get(pk=id_categoria) if id_categoria else None
        )
        return redirect('ver_productos')
    return render(request, 'producto/agregar_producto.html', {'categorias': categorias})

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'producto/actualizar_producto.html', {'producto': producto, 'categorias': categorias})

def realizar_actualizacion_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.nombre = request.POST.get('nombre', producto.nombre)
        stock_raw = request.POST.get('stock')
        try:
            producto.stock = int(stock_raw) if stock_raw not in (None, '') else producto.stock
        except (ValueError, TypeError):
            pass
        producto.descripcion = request.POST.get('descripcion', producto.descripcion)
        precio_raw = request.POST.get('precio')
        try:
            producto.precio = Decimal(precio_raw) if precio_raw not in (None, '') else producto.precio
        except (InvalidOperation, TypeError):
            pass
        id_categoria = request.POST.get('id_categoria')
        producto.id_categoria = Categoria.objects.get(pk=id_categoria) if id_categoria else None
        producto.save()
        return redirect('ver_productos')
    return redirect('ver_productos')

def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})
