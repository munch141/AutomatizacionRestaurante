from django.db import models
from django.contrib.auth.models import User

from proveedor.models import Inventario


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario.username)


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return str(self.nombre)


class Ingrediente_inventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.ingrediente)


class Plato(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    contiene = models.ManyToManyField(Ingrediente, through='Tiene')
    disponible = models.BooleanField()

    def esta_disponible(self, inventario):
        for tiene in self.tiene_set.all():
            if tiene.ingrediente.cantidad < tiene.requiere:
                self.disponible = False
                self.save()
                return False
        
        self.disponible = True
        self.save()
        return True

    def __str__(self):
        return str(self.nombre)


class Tiene(models.Model):
    plato = models.ForeignKey(Plato)
    ingrediente = models.ForeignKey(Ingrediente)
    requiere = models.PositiveIntegerField()


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
