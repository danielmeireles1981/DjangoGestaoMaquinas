from django import forms
from .models import Manutencao

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['maquina', 'data', 'descricao', 'tipo', 'responsavel', 'custo', 'status']