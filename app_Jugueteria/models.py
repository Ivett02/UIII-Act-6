from django.db import models

# ==========================================
# MODELO: SUCURSAL
# ==========================================
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    imagen = models.ImageField(upload_to='sucursales/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"


# ==========================================
# MODELO: CLIENTE (definido pero pendiente)
# ==========================================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="clientes")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: EMPLEADO (definido pero pendiente)
# ==========================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    puesto = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="empleados")

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.puesto}"


# ==========================
# MODELO: CATEGORIA
# ==========================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)          # True = activo
    material = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# ==========================
# MODELO: PRODUCTO
# ==========================
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    def __str__(self):
        return self.nombre
