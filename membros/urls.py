from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_historias'), name='logout'),
    path('perfil/', views.meu_perfil, name='meu_perfil'),
    path('', views.lista_historias, name='lista_historias'),
    path('historias/criar/', views.criar_historia, name='criar_historia'),
    path('historias/editar/<int:id>/', views.editar_historia, name='editar_historia'),
    path('historias/deletar/<int:id>/', views.deletar_historia, name='deletar_historia'),
    path('historia/<int:historia_id>/reagir/<str:tipo>/', views.reagir_historia, name='reagir_historia'),
]