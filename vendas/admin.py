from django.contrib import admin

from vendas.actions import nfe_emitida, nfe_nao_emitida
from vendas.models import Venda, ItemDoPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemDoPedido


class VendaAdmin(admin.ModelAdmin):
    list_filter = ('pessoa__doc', 'desconto')
    list_display = ('id', 'pessoa', 'desconto', 'nfe_emitida')
    search_fields = ('id', 'pessoa__first_name', 'pessoa__doc__num_doc')
    actions = [nfe_emitida, nfe_nao_emitida]
    autocomplete_fields = ('pessoa', )
    inlines = [ItemPedidoInline]
    # raw_id_fields = ('pessoa',)
    # readonly_fields = ('total',)
    # filter_horizontal = ('produtos',)

    def total(self, object):
        total = object.get_total()
        return total

    total.short_description = 'total'


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)

