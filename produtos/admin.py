from django.contrib import admin

from produtos.models import (
    Produto, Estoque, EstoqueEntrada, EstoqueSaida
)

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'valor' ]

# Register your models here.
admin.site.register(Produto)
admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(EstoqueEntrada)
admin.site.register(EstoqueSaida)