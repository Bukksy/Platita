from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.index, name='home'), 
    path('', auth_views.LoginView.as_view(template_name='platita/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('sueldos/', views.sueldos, name='sueldos'),
    path('gastos/', views.gastos, name='gastos'),
    path('gastos/crear/', views.crear_gasto, name='crear_gasto'),
    path('gastos/editar/<int:pk>/', views.editar_gasto, name='editar_gasto'),
    path('gastos/eliminar/<int:pk>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('alimentacion/', views.alimentacion, name="alimentacion"),
    path('alimentacion/crear/', views.crear_compra_alimentacion, name='crear_compra_alimentacion'),
    path('alimentacion/eliminar/<int:pk>/', views.eliminar_compra_alimentacion, name='eliminar_compra'),
    path('planificador/', views.planificador_semanal, name='planificador'),
    path('planificador/sortear/', views.sortear_semana, name='sortear_semana'),
    path('planificador/completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
    path('planificador/extra/', views.agregar_tarea_extra, name='agregar_tarea_extra'),
]