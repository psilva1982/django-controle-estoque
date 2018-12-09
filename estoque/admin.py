from django.contrib import admin

from estoque.models import MovimentoEstoque, Produto
from estoque.models import CategoriaProduto
from estoque.models import SubCategoriaProduto

class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['data_hora', 'tipo_movimento', 'motivo_movimento', 'produto', 'produto_descricao', 'quantidade', 'valor']
    
    def produto_descricao(self, obj):
        return obj.produto.descricao
        
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'descricao', 'valor', 'estoque' ]
    exclude = ('estoque',)

# Register your models here.
admin.site.register(CategoriaProduto)
admin.site.register(SubCategoriaProduto)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(MovimentoEstoque, MovimentoEstoqueAdmin)