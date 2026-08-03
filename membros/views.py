from django.shortcuts import render, redirect, get_object_or_404


from django.contrib import messages


from .forms import HistoriaErroForm
from .models import HistoriaErro


def home(request):
    return render(request, 'home.html')

def lista_historias (request):
    busca = request.GET.get('busca')
    
    if busca:
        historias = HistoriaErro.objects.filter(titulo__icontains=busca)
    else:
        
        historias = HistoriaErro.objects.all().order_by('-data_publicacao')
        
    return render(request, 'meuprimeiro.html', {'historias': historias})

def criar_historia(request):
    
    if request.method == "POST":
        form = HistoriaErroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Confissão publicada com sucesso!')
            return redirect('listar_historias')
        
    else:
        form = HistoriaErroForm()
        return render(request, "criar_membro.html", {"form": form})
    
def editar_historia (request, id):
    historia = get_object_or_404(HistoriaErro, id=id)
    
    if request.method == "POST":
        form = HistoriaErroForm(request.POST, instance=historia)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Historia atualizado com sucesso!')
            return redirect('listar_historias')
            
    else:
        form = HistoriaErroForm (instance=historia)
        
    return render(request, "editar_membro.html", {"form": form, "historia": historia})

def deletar_historia(request, id):
    historia = get_object_or_404 (HistoriaErro, id=id)
    
    if request.method == "POST":
        historia.delete()
        messages.success(request, '🗑️ História apagada para sempre!')
        return redirect ('listar_historias')
    
    return render(request, "confirmar_delecao.html", {"historia": historia})
         