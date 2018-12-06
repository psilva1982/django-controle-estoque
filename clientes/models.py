from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=30)
    cpf = models.CharField(max_length=30, unique=True)
    sobrenome = models.CharField(max_length=30)
    nascimento = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True) 

    def __str__(self):
        return self.cpf