from django.db import models
import django.core.validators

SEXOS = (
     ('M','Masculino'),
     ('F','Femenino')    
)

class Cliente(models.Model):
    ci = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_nacimiento = models.DateTimeField('fecha de nacimiento')
    sexo = models.CharField(max_length=1, choices=SEXOS)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    clave = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.ci)
    