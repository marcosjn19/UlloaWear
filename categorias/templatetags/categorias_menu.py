# categorias/templatetags/categorias_menu.py
from django import template

register = template.Library()

@register.inclusion_tag('categorias/menu_item.html')
def render_categoria(categoria):
    return {'categoria': categoria}
