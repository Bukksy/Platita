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
        ('HOGAR', '🏠 Hogar/Muebles'),  # <--- CATEGORÍA AGREGADA
        ('OTROS', '✨ Otros'),
    ]
    TIPO_GASTO = [
        ('MES', 'Gasto del Mes'),
        ('FIJO', 'Gasto Fijo Mensual'),
        ('FUTURO', 'Gasto Próximo/Planificado'),
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

# 4. Tabla de Ahorro
class MetaAhorro(models.Model):
    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE, related_name='metas', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.IntegerField()
    monto_actual = models.IntegerField(default=0)
    icono = models.CharField(max_length=50, default="bi-piggy-bank")
    
    @property
    def porcentaje(self):
        if self.monto_objetivo > 0:
            p = (self.monto_actual / self.monto_objetivo) * 100
            return min(int(p), 100) 
        return 0

    def __str__(self):
        return f"{self.nombre} ({self.hogar.nombre})"
    
# 5. Registro de sueldo mensual (Lo que se ve en el Dashboard)
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