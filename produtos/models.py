from os.path import isdir

from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

class Produto(models.Model):
    sku = models.CharField(max_length=30, unique=True, null=False, blank=False)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.sku

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    quantidade = models.IntegerField(default=0)

class EstoqueSaida(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    quantidade = models.IntegerField(default=0)

class EstoqueEntrada(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    quantidade = models.IntegerField(default=0)

@receiver(post_save, sender=Produto)
def cria_produto_estoque(sender, instance, **kwargs):
   produto = Produto.objects.get(id=instance.id)
   estoque = Estoque.objects.create(produto=produto)
   estoque.valor = 0.0
   estoque.quantidade = 0
   estoque.save()