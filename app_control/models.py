from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Inspeccionambientes(models.Model):
    ESTADO_CHOICES = [
        ("C", "Correcto"),
        ("O", "Observación"),
    ]

    fecha_registro = models.DateTimeField(auto_now_add=True)
    laboratorio = models.CharField(max_length=50, default="Laboratorio A")
    equipo_computo = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    proyector_multimedia = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    red = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    fluido_electrico = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    orden_limpieza = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    modulos = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.laboratorio} - {self.fecha_registro.strftime('%Y-%m-%d %H:%M')}"