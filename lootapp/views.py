from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mainapp.models import CollectionCategory, Champion
from django.conf import settings
from django.core.cache import cache


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = CollectionCategory.objects.all()
            cache.set(key, categories)
        return categories
    return CollectionCategory.objects.all()


@login_required
def loot(request, name=None):
    context = {
        'title': 'Loot',
        'categories': get_categories(),
        'champions': Champion.objects.all()
    }
    return render(request, 'lootapp/loot.html', context=context)