from django.db import models

SEXOS = (
     ('M','Masculino'),
     ('F','Femenino')    
)

class Cliente(models.Model):
    ci = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_nacimiento = models.DateTimeField('fecha de nacimiento')
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    sexo = models.CharField(max_length=1, choices=SEXOS)
    clave = models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.ci)
    