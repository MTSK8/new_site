from django.db import models

class HistoriaErro(models.Model):
    # Opções de notas de 1 a 5 para usarmos nos níveis
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
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} (Vergonha: {self.nivel_vergonha} | Graça: {self.nivel_graca})"
