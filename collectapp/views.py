from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from mainapp.models import CollectionCategory, Champion, Skin
from basketapp.models import ChampionBasket, SkinBasket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
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
def collection(request, name=None, page=1):

    basket_champ = ChampionBasket.objects.filter(user=request.user).first()
    basket_skin = SkinBasket.objects.filter(user=request.user).first()

    if basket_champ:
        owned_champs = basket_champ.get_owned()

        if basket_skin:
            owned_skins = basket_skin.get_owned()
        else:
            owned_skins = []
    else:
        owned_champs = []
        owned_skins = []

    context = {
        'title': 'Collection',
        'categories': get_categories(),
        'champions': Champion.objects.all().order_by('name'),
        'skins': Skin.objects.all().order_by('champion__name', 'name'),
        'owned_champs': owned_champs,
        'owned_skins': owned_skins,
        'epic_skins': SkinBasket.get_division(owned_skins, 'epic'),
        'legendary_skins': SkinBasket.get_division(owned_skins, 'legendary'),
        'mythic_skins': SkinBasket.get_division(owned_skins, 'mythic'),
        'absolute_skins': SkinBasket.get_division(owned_skins, 'absolute')
    }

    if name == 'champions':
        paginator = Paginator(context['champions'], 12)
        try:
            context['champions'] = paginator.page(page)
        except PageNotAnInteger:
            context['champions'] = paginator.page(1)
        except EmptyPage:
            context['champions'] = paginator.page(paginator.num_pages)
    elif name == 'skins':
        paginator = Paginator(context['skins'], 12)
        try:
            context['skins'] = paginator.page(page)
        except PageNotAnInteger:
            context['skins'] = paginator.page(1)
        except EmptyPage:
            context['skins'] = paginator.page(paginator.num_pages)

    if name is None:
        url = f'collectapp/champions.html'
    else:
        get_object_or_404(CollectionCategory, name=name)
        url = f'collectapp/{name}.html'
        context['title'] = name.title()
    return render(request, url, context=context)


@login_required
def product(request, cat=None, pk=None):

    skins = []

    if cat == "champions":
        product = get_object_or_404(Champion, pk=pk)
        skins = Skin.objects.filter(champion__pk=pk)
    elif cat == "skins":
        product = get_object_or_404(Skin, pk=pk)
        skins = random.sample(list(Skin.objects.all().exclude(pk=pk).select_related()), 5)

    context = {
        'title': product.name,
        'categories': get_categories(),
        'product': product,
        'skins': skins,
        'owned_skins': SkinBasket.objects.filter(user=request.user).values_list('skin', flat=True),
        'owned_champs': ChampionBasket.objects.filter(user=request.user).values_list('champion', flat=True)
    }

    page = f'collectapp/{cat[:-1]}.html'

    return render(request, page, context=context)
