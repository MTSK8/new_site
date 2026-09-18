from django import forms
from .models import HistoriaErro, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class HistoriaErroForm(forms.ModelForm):
    class Meta:
        model = HistoriaErro
        fields = ['titulo', 'descricao', 'autor']
        
        # A propriedade widgets permite customizar como as caixas de texto vão aparecer no HTML
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: O dia em que eu tiver uma diarreia no coletivo'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte todos os detalhes constrangedores aqui...'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Seu apelido (ou deixe em branco para ficar anônimo)'}),
        }
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        
class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']