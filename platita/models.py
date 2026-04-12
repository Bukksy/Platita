from django.db import models
from django.contrib.auth.models import User

# 1. Tabla de Hogar
class Hogar(models.Model):
    nombre = models.CharField(max_length=100, default="Mi Hogar")
    
    def __str__(self):
        return self.nombre

# 2. Tabla de Usuarios
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    hogar = models.ForeignKey(Hogar, on_delete=models.SET_NULL, null=True, blank=True, related_name='integrantes')
    
    # Este sueldo_base es el "maestro" que se copiará a cada mes nuevo
    sueldo_base = models.IntegerField(default=0)
    color_perfil = models.CharField(max_length=7, default="#00bfa5") 
    
    @property
    def sueldo_total(self):
        return self.sueldo_base

    def __str__(self):
        return f"Perfil de {self.usuario.username} - {self.hogar.nombre if self.hogar else 'Sin Hogar'}"

# 3. Tabla de Gastos y Planificación 
class Gasto(models.Model):
    CATEGORIAS = [
        ('ALIMENTACION', '🍎 Alimentación'),
        ('TRANSPORTE', '🚌 Transporte'),
        ('ENTRETENCION', '🎮 Entretenimiento'),
        ('SERVICIOS', '💡 Servicios/Luz/Agua'),
        ('ESTUDIOS', '📚 Estudios/PC'), 
        ('HOGAR', '🏠 Hogar/Muebles'),
        ('OTROS', '✨ Otros'),
    ]
    TIPO_GASTO = [
        ('MES', 'Gasto del Mes'),
        ('FIJO', 'Gasto Fijo Mensual'),
    ]
    
    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE, related_name='gastos')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mis_gastos')
    
    nombre = models.CharField(max_length=100)
    monto = models.IntegerField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='OTROS')
    tipo = models.CharField(max_length=10, choices=TIPO_GASTO, default='MES')
    
    fecha = models.DateField() 
    fecha_registro = models.DateTimeField(auto_now_add=True) 
    comentario = models.TextField(blank=True, null=True) 

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ['-fecha'] 

    def __str__(self):
        return f"{self.nombre} (${self.monto}) - {self.hogar.nombre}"

    
# 4. Sueldoo
class RegistroSueldo(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='registros_sueldos')
    mes = models.PositiveSmallIntegerField()
    anio = models.PositiveIntegerField()
    sueldo_base = models.IntegerField()
    horas_extras = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('perfil', 'mes', 'anio')

    @property
    def total_mes(self):
        return self.sueldo_base + self.horas_extras

    def __str__(self):
        return f"Sueldo {self.perfil.usuario.username} - {self.mes}/{self.anio}"
    
# Tabla para configurar los montos de las tarjetas cada mes
class CargaMensual(models.Model):
    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE, related_name='cargas_mensuales')
    mes = models.PositiveSmallIntegerField()
    anio = models.PositiveIntegerField()
    
    # Montos editables (ponemos los valores estándar como default)
    monto_amipass = models.IntegerField(default=80000)
    monto_junaeb_renato = models.IntegerField(default=48000)
    monto_junaeb_belen = models.IntegerField(default=48000)

    class Meta:
        # Esto evita que tengas dos configuraciones para el mismo mes/hogar
        unique_together = ('hogar', 'mes', 'anio')
        verbose_name = "Carga Mensual"
        verbose_name_plural = "Cargas Mensuales"

    def __str__(self):
        return f"Carga {self.mes}/{self.anio} - {self.hogar.nombre}"


# Tu tabla de Compras de Alimentación (Movimientos)
class CompraAlimentacion(models.Model):
    TARJETAS = [
        ('AMIPASS', '💳 Amipass'),
        ('JUNAEB_R', '🟢 Junaeb Renato'),
        ('JUNAEB_B', '🟣 Junaeb Belén'),
    ]

    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE, related_name='compras_alimentacion')
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)
    monto = models.IntegerField(editable=False) # Se calcula solo
    tarjeta = models.CharField(max_length=20, choices=TARJETAS)
    fecha = models.DateField()

    def save(self, *args, **kwargs):
        self.monto = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Compra Alimentación"
        verbose_name_plural = "Compras Alimentación"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} (${self.monto}) - {self.tarjeta}"