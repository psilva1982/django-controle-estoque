from django.contrib import admin

from estoque.models import EstoqueEntrada, EstoqueSaida


class EstoqueSaidaAdmin(admin.ModelAdmin):
    list_display = ['data_hora', 'produto', 'produto_descricao', 'quantidade', 'valor']

    def produto_descricao(self, obj):
        return obj.produto.descricao 

class EstoqueEntradaAdmin(admin.ModelAdmin):
    list_display = ['data_hora', 'produto', 'produto_descricao', 'quantidade', 'valor']
    
    def produto_descricao(self, obj):
        return obj.produto.descricao 


admin.site.register(EstoqueEntrada, EstoqueEntradaAdmin)
admin.site.register(EstoqueSaida, EstoqueSaidaAdmin)