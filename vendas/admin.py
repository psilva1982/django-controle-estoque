from django.contrib import admin

from vendas.models import ItemVenda, Venda


# Register your models here.
class ItemPedidoInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

class VendaAdmin(admin.ModelAdmin):
    readonly_fields = ('valor',)
    inlines = [ItemPedidoInline]

class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'quantidade']


admin.site.register(Venda, VendaAdmin)
