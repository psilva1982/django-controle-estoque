from django.db import models

from clientes.models import Cliente
from produtos.models import Produto


# Create your models here.
class Venda(models.Model):

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.FloatField(default=0.0, null=False, blank=False)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.produto.descricao