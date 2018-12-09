from django.db import models

from clientes.models import Cliente
from produtos.models import Produto
from estoque.models import MovimentoEstoque
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.db.models import Sum, F, FloatField, Max
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.
class Venda(models.Model):

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    data =  models.DateField(auto_now=False)
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

    def get_total(self):
        tot = self.itemvenda_set.all().aggregate(
            tot_ped=Sum((F('quantidade') * F('produto__valor')) - F('desconto'), output_field=FloatField())
        )['tot_ped'] or 0

        tot = tot - float(self.desconto)
        self.valor = tot
        Venda.objects.filter(id=self.id).update(valor=tot)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.FloatField(default=0.0, null=False, blank=False)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def clean(self):
        if self.quantidade > self.produto.estoque:
            raise ValidationError('Existe(m) apenas {} unidade(s) no estoque do produto {}' .format(self.produto.estoque, self.produto))

    def __str__(self):
        return self.produto.descricao


# Signal para itens da venda
@receiver(post_save, sender=ItemVenda)
def update_total_itens_venda(sender, instance, **kwargs):
    instance.venda.get_total()

# Signal para o cabeçalho da venda
@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance, **kwargs):
    instance.get_total()

@receiver(pre_save, sender=ItemVenda)
def atualiza_estoque(sender, instance, **kwargs):
    
    item_existente = ItemVenda.objects.filter(id=instance.id) 
    produto = instance.produto

    # Se não existe
    if len(item_existente) == 0: 
        produto.estoque -= instance.quantidade
    
         
    # Se existe
    else:
        quantidade_atual = item_existente[0].quantidade
        diferenca = 0

       # Quantidade atual menor que nova quantidade
        if quantidade_atual < instance.quantidade:

            diferenca = instance.quantidade - quantidade_atual
            produto.estoque -= diferenca
        
        elif quantidade_atual > instance.quantidade:
            diferenca = quantidade_atual - instance.quantidade
            produto.estoque += diferenca
            
    produto.save()

