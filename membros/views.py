# Parte de importações

from django.contrib.auth.views import LoginView

from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import login

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import HistoriaErroForm, PerfilForm, CadastroForm

from .models import HistoriaErro, Reacao, Perfil, CadastroPorIP

from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def lista_historias(request):
    busca = request.GET.get('busca', '')

    if busca:
        historias_qs = HistoriaErro.objects.filter(titulo__icontains=busca).order_by('-data_publicacao')
    else:
        historias_qs = HistoriaErro.objects.all().order_by('-data_publicacao')

    paginator = Paginator(historias_qs, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('historias_rows.html', {'historias': page_obj, 'user': request.user}, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        })

    return render(request, 'meuprimeiro.html', {
        'historias': page_obj,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })

@login_required # Garante que só logados criem histórias
def criar_historia(request):
    if request.method == "POST":
        form = HistoriaErroForm(request.POST)
        if form.is_valid():
  
            nova_historia = form.save(commit=False)

            nova_historia.criado_por = request.user

            if not nova_historia.autor:
                nova_historia.autor = "Anônimo"
 
            nova_historia.save()
            
            messages.success(request, '🎉 Confissão publicada com sucesso!')
            return redirect('lista_historias')
    else:
        form = HistoriaErroForm()
        
    return render(request, "confessar_erro.html", {"form": form})
    
@login_required    
def editar_historia(request, id):
    historia = get_object_or_404(HistoriaErro, id=id)
    
   
    if historia.criado_por.id != request.user.id:
        messages.error(request, "🚫 Ei seu intruso voce só pode editar as suas próprias histórias!!! 🚫")
        return redirect('lista_historias')
    
    if request.method == "POST":
        form = HistoriaErroForm(request.POST, instance=historia)
        if form.is_valid():
            historia_editada = form.save(commit=False)
            if not historia_editada.autor:
                historia_editada.autor = "Anônimo"
            historia_editada.save()
            
            messages.success(request, '✏️ História atualizada com sucesso!')
            return redirect('lista_historias')
    else:
        form = HistoriaErroForm(instance=historia)
        
    return render(request, "editar_historia.html", {"form": form, "historia": historia})

@login_required
def deletar_historia(request, id):
    historia = get_object_or_404(HistoriaErro, id=id)
    
    if historia.criado_por.id != request.user.id:
        messages.error(request, "🚫 Ei seu intruso, Você não pode apagar as histórias alheias!")
        return redirect('lista_historias')
    
    if request.method == "POST":
        historia.delete()
        messages.success(request, '🗑️ História apagada para sempre!')
        return redirect('lista_historias')
    
    return render(request, "confirmar_delecao.html", {"historia": historia})


@login_required
def reagir_historia(request, historia_id, tipo):
    historia = get_object_or_404(HistoriaErro, id=historia_id)

    if historia.criado_por == request.user:
        return redirect(request.META.get('HTTP_REFERER', 'lista_historias'))

    reacao = Reacao.objects.filter(historia=historia, usuario=request.user).first()

    if reacao:
        if reacao.tipo == tipo:
            reacao.delete()  
        else:
            reacao.tipo = tipo  
            reacao.save()
    else:
        Reacao.objects.create(historia=historia, usuario=request.user, tipo=tipo)

    return redirect(request.META.get('HTTP_REFERER', 'lista_historias'))


LIMITE_CADASTROS_POR_IP = 2


def get_client_ip(request):
    # Sem proxy reverso configurado ainda — REMOTE_ADDR é confiável aqui.
    # Se um dia isso ficar atrás de Nginx/Gunicorn, revisamos pra usar o
    # cabeçalho X-Forwarded-For (só se o proxy garantir que ele não pode
    # ser falsificado pelo próprio visitante).
    return request.META.get('REMOTE_ADDR')


def registrar_usuario(request):
    ip = get_client_ip(request)

    if CadastroPorIP.objects.filter(ip=ip).count() >= LIMITE_CADASTROS_POR_IP:
        messages.error(request, '🚫 Limite de contas criadas a partir deste endereço foi atingido.')
        return redirect('login')

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            CadastroPorIP.objects.create(ip=ip)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Bem-Vindo(a), {user.username}! Conta criada com sucesso.")
            return redirect('lista_historias')
    else:
        form = CadastroForm()

    return render(request, 'registro.html', {'form': form})

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = "Bem-vindo de volta, %(username)s! 😎"
    
    
@login_required
def meu_perfil(request):
    # essa parte aqui Filtra apenas as histórias onde o 'criado_por' é o usuário atual
    historias_qs = HistoriaErro.objects.filter(criado_por=request.user).order_by('-data_publicacao')

    
    paginator = Paginator(historias_qs, 3)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        html = render_to_string('historias_rows.html', {'historias': page_obj, 'user': request.user}, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        })

    #Aqui renderiza a página base do perfil
    return render(request, 'perfil.html', {
        'historias': page_obj,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })
    
@login_required
def editar_perfil(request):
    perfil, criado = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, '📸 Foto de perfil atualizada!')
            return redirect('meu_perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'editar_perfil.html', {'form': form})
            