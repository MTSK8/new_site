from django.db import models
from django.contrib.auth.models import User

class HistoriaErro(models.Model):
   
    NOTAS_CHOICES = [
        (1, '1 - Muito baixo'),
        (2, '2 - Baixo'),
        (3, '3 - Médio'),
        (4, '4 - Alto'),
        (5, '5 - Extremo')
    ]

    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    nivel_vergonha = models.IntegerField(choices=NOTAS_CHOICES)
    nivel_graca = models.IntegerField(choices=NOTAS_CHOICES)
    autor = models.CharField(max_length=100, blank=True, null=True)
    
    
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} (Vergonha: {self.nivel_vergonha} | Graça: {self.nivel_graca})"
    
    
class Reacao(models.Model):
    TIPOS = [
        ('graca', '😂 Engraçado'),
        ('vergonha', '😳 Vergonha'),
    ]
        
    historia = models.ForeignKey(HistoriaErro, on_delete=models.CASCADE, related_name='reacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
        
    class Meta:
        unique_together = ('historia', 'usuario')