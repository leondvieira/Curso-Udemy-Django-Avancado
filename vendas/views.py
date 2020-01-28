from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Sum, F, FloatField, Max, Avg, Min, Count

from vendas.models import Venda


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
