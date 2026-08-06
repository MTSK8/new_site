from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_historias, name='lista_historias'),
    path('historias/criar/', views.criar_historia, name='criar_historia'),
    path('historias/editar/<int:id>/', views.editar_historia, name='editar_historia'),
    path('historias/deletar/<int:id>/', views.deletar_historia, name='deletar_historia'),
]