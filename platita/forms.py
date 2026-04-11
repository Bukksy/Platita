from django import forms
from .models import Gasto, MetaAhorro

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

class MetaAhorroForm(forms.ModelForm):
    class Meta:
        model = MetaAhorro
        fields = ['nombre', 'monto_objetivo', 'icono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Notebook Pro'}),
            'monto_objetivo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto total'}),
            'icono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-laptop'}),
        }