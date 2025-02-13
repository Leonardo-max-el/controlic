from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# cambiar el laoratorio por ambientes

class Inspeccionambientes(models.Model):
    ESTADO_CHOICES = [
        ("C", "Correcto"),
        ("O", "Observación"),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    laboratorio = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    equipo_computo = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    proyector_multimedia = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    red = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    fluido_electrico = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    orden_limpieza = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    modulos = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    observacion = models.TextField(max_length=200, default="NO SE ENCONTRARON OBSERVACIONES", blank=True)

    def __str__(self):
        return f"{self.laboratorio} - {self.fecha_registro.strftime('%Y-%m-%d')}"