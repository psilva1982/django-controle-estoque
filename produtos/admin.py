from django.contrib import admin
from produtos.models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'descricao', 'valor', 'estoque' ]



# Register your models here.
admin.site.register(Produto, ProdutoAdmin)
