from django.contrib import admin

from estoque.models import MovimentoEstoque


class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['data_hora', 'tipo_movimento', 'motivo_movimento', 'produto', 'produto_descricao', 'quantidade', 'valor']
    
    def produto_descricao(self, obj):
        return obj.produto.descricao 


admin.site.register(MovimentoEstoque, MovimentoEstoqueAdmin)