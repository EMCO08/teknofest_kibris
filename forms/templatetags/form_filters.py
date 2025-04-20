from django import template

register = template.Library()

@register.filter
def get_dict_item(dictionary, key):
    """Sözlük elemanına erişim için template filtresi"""
    if not dictionary:
        return None
    if key in dictionary:
        return dictionary[key]
    return None 