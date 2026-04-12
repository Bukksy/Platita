from django import forms
from .models import Gasto, CompraAlimentacion, CargaMensual

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['nombre', 'monto', 'categoria', 'tipo', 'fecha', 'comentario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Supermercado'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 50000'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Opcional...'}),
        }

class GastoAlimentacionForm(forms.ModelForm):
    class Meta:
        model = CompraAlimentacion
        fields = ['nombre', 'cantidad', 'precio_unitario', 'tarjeta', 'fecha']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Arroz'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cantidad'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_precio_u'}),
            'tarjeta': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CargaMensualForm(forms.ModelForm):
    class Meta:
        model = CargaMensual
        fields = ['monto_amipass', 'monto_junaeb_renato', 'monto_junaeb_belen']
        widgets = {
            'monto_amipass': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_junaeb_renato': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_junaeb_belen': forms.NumberInput(attrs={'class': 'form-control'}),
        }