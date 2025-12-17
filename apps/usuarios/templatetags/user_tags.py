from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from apps.posts.models import Post

register = template.Library()

@register.simple_tag
def get_colaboradores_activos(limit=5):
    """
    Obtiene los colaboradores más activos basado en posts publicados.
    """
    User = get_user_model()
    
    # Filtrar usuarios colaboradores con posts publicados
    colaboradores = User.objects.filter(
        Q(colaborador=True) | Q(is_staff=True) | Q(is_superuser=True)
    ).annotate(
        post_count=Count('post', filter=Q(post__estado='publicado'))
    ).filter(
        post_count__gt=0
    ).order_by('-post_count')[:limit]
    
    return colaboradores

@register.filter(name='puede_crear_post')
def puede_crear_post(user):
    """
    Verifica si un usuario puede crear posts.
    """
    if not user.is_authenticated:
        return False
    
    # Usa getattr para evitar errores si el campo no existe
    es_colaborador = getattr(user, 'colaborador', False)
    return es_colaborador or user.is_staff or user.is_superuser

@register.simple_tag
def contar_colaboradores():
    """
    Cuenta el total de colaboradores activos.
    """
    User = get_user_model()
    return User.objects.filter(
        Q(colaborador=True) | Q(is_staff=True) | Q(is_superuser=True)
    ).count()