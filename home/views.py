from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.views.generic import TemplateView

from django.http import HttpResponse
from django.views import View


def home(request):
    return render(request, 'home/home.html')


def my_logout(request):
    logout(request)
    return redirect('home')


class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minha_variavel'] = 'Bem vindo a pagina 3 do curso de django advanced'
        return context


class MyView(View):

    def get(self, request, *args, **kwargs):
        response = render_to_response('home3.html')
        response.set_cookie('color', 'blue', max_age=1000)
        return response

    def post(self, request, *args, **kwargs):
        return HttpResponse('Post')