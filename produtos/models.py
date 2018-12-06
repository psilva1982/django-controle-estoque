from astroid import objects
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

class Produto(models.Model):
    sku = models.CharField(max_length=30, unique=True, null=False, blank=False)
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    estoque = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    
    def __str__(self):
        return self.sku
