from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Gasto, Perfil, MetaAhorro, RegistroSueldo
from django.utils import timezone

@login_required
def index(request):
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    if mes_actual == 12:
        mes_prox, anio_prox = 1, anio_actual + 1
    else:
        mes_prox, anio_prox = mes_actual + 1, anio_actual

    meses_nombres = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    integrantes_actual = RegistroSueldo.objects.filter(mes=mes_actual, anio=anio_actual)
    integrantes_proximo = RegistroSueldo.objects.filter(mes=mes_prox, anio=anio_prox)

    context = {
        'nombre_mes_actual': meses_nombres[mes_actual - 1],
        'nombre_mes_proximo': meses_nombres[mes_prox - 1],
        'integrantes': integrantes_actual,
        'integrantes_proximo': integrantes_proximo,
        'total_ingresos': sum(i.total_mes for i in integrantes_actual),
        'total_proximo': sum(i.total_mes for i in integrantes_proximo),
    }
    return render(request, 'platita/index.html', context)

@login_required
def sueldos(request):
    perfil = Perfil.objects.get(usuario=request.user)
    mes_actual = int(request.GET.get('mes', timezone.now().month))
    anio_actual = timezone.now().year
    
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    registro, created = RegistroSueldo.objects.get_or_create(
        perfil=perfil, 
        mes=mes_actual, 
        anio=anio_actual,
        defaults={'sueldo_base': perfil.sueldo_total or 0}
    )

    if request.method == 'POST':
        registro.sueldo_base = float(request.POST.get('sueldo_base', 0))
        registro.horas_extras = float(request.POST.get('horas_extras', 0))
        registro.save()
        return redirect(f'/sueldos/?mes={mes_actual}')

    context = {
        'perfil': perfil,
        'registro': registro,
        'mes_nombre': meses_nombres[mes_actual-1],
        'meses_lista': enumerate(meses_nombres, 1)
    }
    return render(request, 'platita/sueldos.html', context)