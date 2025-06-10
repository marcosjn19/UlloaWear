from django import template

register = template.Library()

@register.inclusion_tag('menu_item.html', takes_context=True)
def render_categoria(context, categoria):
    return {
        'categoria': categoria,
        'request': context.get('request'),
    }
