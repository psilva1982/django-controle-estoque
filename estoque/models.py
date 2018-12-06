from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

from produtos.models import Produto


class EstoqueSaida(models.Model):

    VENDA = 'vd'
    DEVOLUCAO_FABRICANTE = 'df'
    OUTROS = 'ou'

    TIPO_SAIDA = (
        (VENDA, 'Venda'),
        (DEVOLUCAO_FABRICANTE, 'Devolução para fábrica'),
        (OUTROS, 'Outros')
    )

    data_hora = models.DateTimeField(auto_created=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    saida = models.CharField(choices=TIPO_SAIDA, default=VENDA, max_length=2)
    quantidade = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Saída do estoque'
        verbose_name_plural = 'saída do estoque'

    def clean(self):
        
        saldo_estoque = self.produto.estoque - self.quantidade
        if saldo_estoque < 0:
            raise ValidationError('Existe(m) apenas {} unidade(s) no estoque' .format(self.produto.estoque))
    
class EstoqueEntrada(models.Model):

    COMPRA = 'dv'
    CANCELAMENTO = 'dv'
    OUTROS = 'ou'

    TIPO_ENTRADA = (
        (COMPRA, 'Compra'),
        (CANCELAMENTO, 'Cancelamento de venda'),
        (OUTROS, 'Outros')
    )

    data_hora = models.DateTimeField(auto_created=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    entrada = models.CharField(choices=TIPO_ENTRADA, default=COMPRA, max_length=2)
    quantidade = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'entrada no estoque'
        verbose_name_plural = 'entrada no estoque'

@receiver(post_save, sender=EstoqueEntrada)
def atualiza_estoque_pela_entrada(sender, instance, **kwargs):
    produto = instance.produto
    produto.estoque += instance.quantidade
    produto.valor = instance.valor
    produto.save()

@receiver(post_save, sender=EstoqueSaida)
def atualiza_estoque_pela_saida(sender, instance, **kwargs):
    produto = instance.produto
    produto.estoque -= instance.quantidade
    produto.save()