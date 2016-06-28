from django.db import models
from django.contrib.auth.models import User


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario.username)


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    descripcion = models.TextField()
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.nombre)


class Plato(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    contiene = models.ManyToManyField(Ingrediente)

    def __str__(self):
        return str(self.nombre)

    def __str__(self):
        return str(self.nombre)


class Menu(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    actual = models.BooleanField(default=False)
    incluye = models.ManyToManyField(Plato)

    def save(self, *args, **kwargs):
        if self.actual:
            try:
                temp = Menu.objects.get(actual=True)
                if self != temp:
                    temp.actual = False
                    temp.save()
            except Menu.DoesNotExist:
                pass
        super(Menu, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.nombre)
