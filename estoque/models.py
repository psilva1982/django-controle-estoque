from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_save, pre_delete
from django.dispatch import receiver

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
class SubCategoriaProduto(models.Model):
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria.nome+ ' \ ' +self.nome

class Produto(models.Model):
    sku = models.CharField(max_length=30, unique=True, null=False, blank=False)
    descricao = models.CharField(max_length=150)
    subcategoria = models.ForeignKey(SubCategoriaProduto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    estoque = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    
    def __str__(self):
        return self.sku + ' - ' + self.descricao
class MovimentoEstoque(models.Model):

    VENDA = 'vd'
    COMPRA = 'cp'
    DEVOLUCAO_FABRICANTE = 'df'
    CANCELAMENTO = 'dv'
    OUTROS = 'ou'

    ENTRADA = 'en'
    SAIDA = 'sd'

    TIPO_MOVIMENTO = (
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída')
    )

    MOTIVO_MOVIMENTO = (
        (VENDA, 'Venda'),
        (COMPRA, 'Compra para revenda'),
        (CANCELAMENTO, 'Cancelamento de venda'),
        (OUTROS, 'Outros')
    )

    data_hora = models.DateTimeField(auto_created=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    numero = models.CharField(max_length=30, null=True, blank=True)
    tipo_movimento = models.CharField(choices=TIPO_MOVIMENTO, default=SAIDA, max_length=2)
    motivo_movimento = models.CharField(choices=MOTIVO_MOVIMENTO, default=VENDA, max_length=2)
    quantidade = models.IntegerField(default=0)

    def clean(self):
        if self.quantidade > self.produto.estoque and self.tipo_movimento == 'sd':
            raise ValidationError('Existe(m) apenas {} unidade(s) no estoque do produto {}' .format(self.produto.estoque, self.produto))

    class Meta:
        verbose_name = 'Movimento do estoque'
        verbose_name_plural = 'Movimento do estoque'

@receiver(pre_save, sender=MovimentoEstoque)
def atualiza_estoque(sender, instance, **kwargs):
    
    movimento = MovimentoEstoque.objects.filter(id=instance.id) 
    produto = instance.produto

    # Se o movimento não existe
    if len(movimento) == 0: 

        if instance.tipo_movimento == 'en' : 
            produto.estoque += instance.quantidade

        else :
            produto.estoque -= instance.quantidade
    
    else:
        quantidade_atual = movimento[0].quantidade
        
        if instance.tipo_movimento == 'en' :
            if quantidade_atual < instance.quantidade:

                diferenca = instance.quantidade - quantidade_atual
                produto.estoque += diferenca   
            
            else:
                diferenca = quantidade_atual - instance.quantidade
                produto.estoque -= diferenca   

        else:
            if quantidade_atual < instance.quantidade:

                diferenca = instance.quantidade - quantidade_atual
                produto.estoque -= diferenca   
            
            else:
                diferenca = quantidade_atual - instance.quantidade
                produto.estoque += diferenca            
           
            
    produto.save()

@receiver(pre_delete, sender=MovimentoEstoque)
def remove_movimento(sender, instance, **kwargs):
    produto = instance.produto 
    if instance.tipo_movimento == 'en' :
        produto.estoque -= instance.quantidade
    
    else:
        produto.estoque += instance.quantidade
    
    produto.save()