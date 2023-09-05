from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from lootapp.models import PurchasedMaterial
from mainapp.models import CollectionCategory, Champion, Skin
from basketapp.models import ChampionBasket, SkinBasket
from django.db.models import Q
from django.http import Http404
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
def store(request, name=None, role='all'):

    basket_champ = ChampionBasket.objects.filter(user=request.user).first()
    basket_skin = SkinBasket.objects.filter(user=request.user).first()

    if basket_champ:
        owned_champs = basket_champ.get_owned()
        champ_total_cost_rp = basket_champ.get_total_cost[0]
        champ_total_cost_be = basket_champ.get_total_cost[1]

        if basket_skin:
            owned_skins = basket_skin.get_owned()
            skin_total_cost = basket_skin.get_total_cost
        else:
            owned_skins = SkinBasket.objects.none()
            skin_total_cost = 0
    else:
        owned_champs = ChampionBasket.objects.none()
        owned_skins = SkinBasket.objects.none()
        champ_total_cost_rp = 0
        champ_total_cost_be = 0
        skin_total_cost = 0

    material_total_cost = sum(map(lambda x: x.get_total_cost, PurchasedMaterial.objects.filter(user=request.user)))

    total_cost_rp = champ_total_cost_rp + skin_total_cost + material_total_cost

    roles = {
        'slayer': ['assassin', 'skirmisher'],
        'fighter': ['juggernaut', 'diver'],
        'mage': ['battlemage', 'burst', 'artillery'],
        'marksman': ['marksman'],
        'tank': ['vanguard', 'warden'],
        'support': ['catcher', 'enchanter']
    }

    context = {
        'title': 'Store',
        'categories': get_categories(),
        'champions': Champion.objects.filter(~Q(pk__in=owned_champs)).order_by('name'),
        'roles': roles,
        'skins': Skin.objects.filter(~Q(pk__in=owned_skins)).order_by('champion__name', 'name'),
        'owned_champs': owned_champs,
        'owned_skins': owned_skins,
        'total_cost_rp': total_cost_rp,
        'total_cost_be': champ_total_cost_be
    }

    if role != 'all':

        if role not in roles:
            raise Http404

        name = 'champions'

        champions = context['champions'].filter(Q(role__in=roles[role]) | Q(role_b__in=roles[role]))
        context['champions'] = champions

    if name is None:
        page = 'storeapp/store.html'
    elif name == 'loot':
        page = 'storeapp/loot.html'
    else:
        get_object_or_404(CollectionCategory, name=name)
        page = f'storeapp/{name}.html'
        context['title'] = name.title()

    return render(request, page, context=context)


@login_required
def add(request, cat=None, pk=None):

    if cat == "champions":
        product = get_object_or_404(Champion, pk=pk)
    elif cat == "skins":
        product = get_object_or_404(Skin, pk=pk)

    context = {
        'title': product.name,
        'product': product,
        'owned_skins': SkinBasket.objects.filter(user=request.user).values_list('skin', flat=True),
        'owned_champs': ChampionBasket.objects.filter(user=request.user).values_list('champion', flat=True)
    }

    page = f'storeapp/{cat[:-1]}.html'

    return render(request, page, context=context)