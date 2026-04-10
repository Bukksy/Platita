from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import Gasto, RegistroSueldo, Perfil
from .forms import GastoForm

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
    hogar = request.user.perfil.hogar
    # Obtenemos todos los perfiles que pertenecen al mismo hogar
    integrantes = Perfil.objects.filter(hogar=hogar)
    
    # Determinamos qué perfil se va a editar (por defecto el del usuario logueado)
    perfil_id = request.GET.get('perfil_id', request.user.perfil.id)
    perfil_seleccionado = get_object_or_404(Perfil, id=perfil_id, hogar=hogar)
    
    mes_actual = int(request.GET.get('mes', timezone.now().month))
    anio_actual = timezone.now().year
    
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    # Buscamos o creamos el registro para el perfil seleccionado (sea Renato o Belén)
    registro, created = RegistroSueldo.objects.get_or_create(
        perfil=perfil_seleccionado, 
        mes=mes_actual, 
        anio=anio_actual,
        defaults={'sueldo_base': perfil_seleccionado.sueldo_total or 0}
    )

    if request.method == 'POST':
        registro.sueldo_base = float(request.POST.get('sueldo_base', 0))
        registro.horas_extras = float(request.POST.get('horas_extras', 0))
        registro.save()
        # Redirigimos manteniendo el perfil y el mes que se estaba editando
        return redirect(f'/sueldos/?perfil_id={perfil_id}&mes={mes_actual}')

    context = {
        'perfil_sel': perfil_seleccionado,
        'integrantes': integrantes,
        'registro': registro,
        'mes_nombre': meses_nombres[mes_actual-1],
        'meses_lista': enumerate(meses_nombres, 1)
    }
    return render(request, 'platita/sueldos.html', context)

@login_required
def gastos(request):
    hogar = request.user.perfil.hogar
    hoy = timezone.now()
    
    mes_actual = int(request.GET.get('mes', hoy.month))
    anio_raw = str(request.GET.get('anio', hoy.year)).replace('\xa0', '').replace(' ', '')
    anio_actual = int(float(anio_raw))

    registros = RegistroSueldo.objects.filter(perfil__hogar=hogar, mes=mes_actual, anio=anio_actual)
    total_sueldos = registros.aggregate(s_base=Sum('sueldo_base'), s_extras=Sum('horas_extras'))
    ingreso_total = float((total_sueldos['s_base'] or 0) + (total_sueldos['s_extras'] or 0))

    gastos_fijos = Gasto.objects.filter(hogar=hogar, tipo='FIJO')
    gastos_mes = Gasto.objects.filter(hogar=hogar, tipo='MES', fecha__month=mes_actual, fecha__year=anio_actual)

    total_fijos = float(gastos_fijos.aggregate(total=Sum('monto'))['total'] or 0)
    total_variables = float(gastos_mes.aggregate(total=Sum('monto'))['total'] or 0)
    
    total_gastos = total_fijos + total_variables
    saldo_restante = ingreso_total - total_gastos
    porcentaje = (total_gastos / ingreso_total * 100) if ingreso_total > 0 else 0

    meses_opciones = []
    meses_restantes = 12 - hoy.month + 1
    
    for i in range(0, meses_restantes):
        m_proyectado = hoy.month + i
        a_proyectado = hoy.year
        
        fecha_temp = date(a_proyectado, m_proyectado, 1)
        
        meses_opciones.append({
            'n': m_proyectado,
            'a': a_proyectado,
            'nombre': fecha_temp.strftime('%b').capitalize()
        })

    context = {
        'gastos_fijos': gastos_fijos,
        'gastos_mes': gastos_mes,
        'ingreso_total': ingreso_total,
        'total_gastos': total_gastos,
        'saldo_restante': saldo_restante,
        'porcentaje': min(round(porcentaje, 2), 100),
        'mes_nombre': datetime(anio_actual, mes_actual, 1).strftime('%B').capitalize(),
        'mes_sel': mes_actual,
        'anio_sel': anio_actual,
        'meses_opciones': meses_opciones,
        'form': GastoForm(initial={'fecha': date(anio_actual, mes_actual, 1)}),
    }
    return render(request, 'platita/gastos.html', context)

@login_required
def crear_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.creado_por = request.user
            gasto.hogar = request.user.perfil.hogar
            gasto.save()
    return redirect('gastos')

@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk, hogar=request.user.perfil.hogar)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('gastos')
    # Si quieres una página aparte para editar, podrías retornarla aquí, 
    # pero por ahora lo manejaremos simple.
    return redirect('gastos')

@login_required
def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk, hogar=request.user.perfil.hogar)
    gasto.delete()
    return redirect('gastos')

@login_required
def ahorro(request):
    return render(request, 'platita/ahorros.html')