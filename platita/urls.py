from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('', auth_views.LoginView.as_view(template_name='platita/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('sueldos/', views.sueldos, name='sueldos'),
]