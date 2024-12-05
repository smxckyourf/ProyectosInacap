from django import template

register = template.Library()

@register.filter
def pertenece_a_grupo(user, group_name):
    """
    Verifica si el usuario pertenece al grupo especificado.
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False