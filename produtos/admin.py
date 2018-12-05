from django.contrib import admin

from produtos.models import (
    Produto, Estoque, EstoqueEntrada, EstoqueSaida
)

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'produto_descricao', 'quantidade', 'valor' ]

    def produto_descricao(self, obj):
        return obj.produto.descricao 

# Register your models here.
admin.site.register(Produto)
admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(EstoqueEntrada)
admin.site.register(EstoqueSaida)