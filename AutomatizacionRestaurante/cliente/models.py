from django.db import models
from cuentas.models import Cliente


class BilleteraElectronica(models.Model):
	usuario = models.OneToOneField(Cliente, on_delete = models.CASCADE, primary_key=True,)
	debitos = []
	creditos = []
	pin = models.CharField(max_length=6,)

	def __str__(self):
		return str(self.pin)
