from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView, View

from produtos.models import Produto
from vendas.models import Venda
from .models import Person
from .forms import PersonForm


@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    if not request.user.has_perm('cliente.add_person'):
        return HttpResponse('Não autorizado')
    elif not request.user.is_superuser:
        return HttpResponse('Não é superusuario')

    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})


class PersonList(LoginRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        primeiro_acesso = self.request.session.get('primeiro_acesso', False)

        if not primeiro_acesso:
            context['message'] = 'Seja bem vindo ao seu primeiro acesso hoje!'
            self.request.session['primeiro_acesso'] = True
        else:
            context['message'] = 'Bem vindo novamente!'

        return context


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Person.objects.select_related('doc').get(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['vendas'] = Venda.objects.filter(
            pessoa_id=self.object.id
        )
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    fields = '__all__'

    success_url = reverse_lazy('person_list_cbv')


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person
    fields = '__all__'
    success_url = reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Person

    permission_required = ('clientes.deletar_clientes',)

    # success_url utilizado para redirecionamento simples
    # success_url = reverse_lazy('person_list_cbv')

    # utilizado para passar paramentros, verificar permissoes, etc
    def get_success_url(self):
        return reverse_lazy('person_list_cbv')


class ProdutoBulk(View):

    def get(self, request):
        produtos = ['Banana', 'Laranja', 'Tomate', 'Cebola', 'Uva']
        lista_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            lista_produtos.append(p)

        Produto.objects.bulk_create(lista_produtos)

        return HttpResponse('Funcionou')