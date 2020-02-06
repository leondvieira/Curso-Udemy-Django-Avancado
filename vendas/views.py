from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum, F, FloatField, Max, Avg, Min, Count

from vendas.forms import ItemPedidoForm
from vendas.models import Venda, ItemDoPedido


class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Acesso negado!')
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {}
        data['media'] = Venda.objects.media()
        data['media_desc'] = Venda.objects.media_desconto()
        data['min'] = Venda.objects.min()
        data['max'] = Venda.objects.max()
        data['num_pedidos'] = Venda.objects.num_pedidos()
        data['num_ped_nefe'] = Venda.objects.num_ped_nefe()

        return render(request, 'vendas/dashboard.html', data)


class NovoPedido(View):
    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        data = {}
        data['numero'] = request.POST['numero']
        data['venda'] = request.POST['venda_id']

        if data['numero']:
            venda = Venda.objects.get(numero=data['numero'])
        else:
            venda = Venda.objects.create(
                numero=data['numero']
            )

        itens = venda.itemdopedido_set.all()
        data['venda_obj'] = venda
        data['itens'] = itens
        return render(
            request, 'vendas/novo-pedido.html', data
        )


class NovoItemPedido(View):

    def get(self, request, pk):
        pass

    def post(self, request, venda):
        data = {}
        item = ItemDoPedido.objects.create(
            produto_id=request.POST['produto_id'], quantidade=request.POST['quantidade'],
            desconto=request.POST['desconto'], venda_id=venda
        )

        data['item'] = item
        data['form_item'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda.id
        data['venda_obj'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(
            request, 'vendas/novo-pedido.html', data
        )


class ListaVendas(View):
    def get(self, request):
        vendas = Venda.objects.all()
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas})


class EditPedido(View):
    def get(self, request, venda):
        data = {}
        venda = Venda.objects.get(id=venda)
        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemdopedido_set.all()

        return render(
            request, 'vendas/novo-pedido.html', data
        )


class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(request, 'vendas/confirm-delete.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')