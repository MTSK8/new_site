from django import template
register = template.Library()

@register.filter
def contar_tipo(reacoes, tipo):
    return reacoes.filter(tipo=tipo).count()