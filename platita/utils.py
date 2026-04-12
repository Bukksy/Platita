import random
from datetime import date, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from .models import TareaAsignada, TareaMaestra

def generar_plan_semanal():
    u1 = User.objects.filter(username__iexact='renato').first()
    u2 = User.objects.filter(username__iexact='belen').first()
    
    if not u1 or not u2:
        return
    
    usuarios = [u1, u2]
    hoy = date.today()
    lunes = hoy + timedelta(days=1) if hoy.weekday() == 6 else hoy - timedelta(days=hoy.weekday())
    
    with transaction.atomic():
        TareaAsignada.objects.filter(fecha_semana=lunes, tarea__isnull=False).delete()
        
        tareas_fijas = TareaMaestra.objects.all()
        if not tareas_fijas.exists():
            return

        dias_codigos = ['LU', 'MA', 'MI', 'JU', 'VI', 'SA', 'DO']
        plan_diario = {dia: [] for dia in dias_codigos}
        
        arenero = tareas_fijas.filter(nombre__icontains='arenero').first()
        otras_fijas = tareas_fijas.exclude(id=arenero.id if arenero else None)

        for tm in otras_fijas:
            if tm.es_diaria:
                dias_destinatarios = dias_codigos
            else:
                frec = min(tm.frecuencia_semanal, 7)
                dias_destinatarios = random.sample(dias_codigos, frec)
            
            for d in dias_destinatarios:
                plan_diario[d].append(tm)

        ultimo_en_partir = random.choice(usuarios)

        for d in dias_codigos:
            # El que NO partió ayer, parte hoy con el arenero
            quien_parte = u2 if ultimo_en_partir == u1 else u1
            quien_sigue = u1 if quien_parte == u2 else u2
            
            if arenero:
                TareaAsignada.objects.create(
                    tarea=arenero,
                    dia=d,
                    responsable=quien_parte,
                    fecha_semana=lunes
                )

            tareas_del_dia = plan_diario[d]
            random.shuffle(tareas_del_dia)
            
            # Repartimos el resto empezando por la otra persona para asegurar que ambos trabajen
            for i, tm in enumerate(tareas_del_dia):
                # Si es la primera tarea extra, le toca al que NO hizo el arenero
                responsable = quien_sigue if i % 2 == 0 else quien_parte
                
                TareaAsignada.objects.create(
                    tarea=tm,
                    dia=d,
                    responsable=responsable,
                    fecha_semana=lunes
                )
            
            ultimo_en_partir = quien_parte

        extras_sin_dueno = TareaAsignada.objects.filter(
            fecha_semana=lunes, 
            tarea__isnull=True, 
            responsable__isnull=True
        )
        for extra in extras_sin_dueno:
            extra.responsable = random.choice(usuarios)
            extra.save()