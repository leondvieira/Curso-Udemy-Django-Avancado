from django.urls import path
from django.views.generic import TemplateView

from .views import home, my_logout, HomePageView, MyView

urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),
    path('home2/', TemplateView.as_view(template_name='home2.html')),
    path('home3/', HomePageView.as_view()),
    path('view', MyView.as_view())
]