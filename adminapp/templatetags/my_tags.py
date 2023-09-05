from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='icon_default')
def icon_default(icon):
    if not icon:
        icon = f'{settings.MEDIA_URL}/icons/Gromp.png'
    return icon


@register.filter(name='loot')
def loot(item):
    return f'{settings.MEDIA_URL}/{item}'
