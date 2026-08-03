from django import forms
from .models import HistoriaErro

class HistoriaErroForm(forms.ModelForm):
    class Meta:
        model = HistoriaErro
        fields = ['titulo', 'descricao', 'nivel_vergonha', 'nivel_graca', 'autor']
        
        # A propriedade widgets permite customizar como as caixas de texto vão aparecer no HTML
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: O dia em que eu tiver uma diarreia no coletivo'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte todos os detalhes constrangedores aqui...'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Seu apelido (ou deixe em branco para ficar anônimo)'}),
        }