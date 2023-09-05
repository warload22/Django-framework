from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from basketapp.models import ChampionBasket, SkinBasket
from django.urls import reverse
from mainapp.models import Champion, Skin


@login_required
def add(request, cat=None, pk=None, method='rp'):

    if cat == 'champions':
        champ = get_object_or_404(Champion, pk=pk)

        if not ChampionBasket.objects.filter(champion=champ, user=request.user):
            basket_item = ChampionBasket(champion=champ, user=request.user, method=method)
            basket_item.save()

            if method == 'rp':
                request.user.subtract_rp(champ.price_rp)
            else:
                request.user.subtract_be(champ.price_be)

    elif cat == 'skins':
        skin = get_object_or_404(Skin, pk=pk)

        if not SkinBasket.objects.filter(skin=skin, user=request.user) \
                and ChampionBasket.objects.filter(champion=skin.champion, user=request.user):
            basket_item = SkinBasket(skin=skin, user=request.user, champion=skin.champion)
            basket_item.save()

        if method == 'rp':
            request.user.subtract_rp(skin.price_rp)
        else:
            request.user.subtract_be(skin.price_be)

    return HttpResponseRedirect(reverse('store:category', kwargs={'name': cat}))


@login_required
def remove(request, cat=None, pk=None):

    if cat == 'champions':
        champ = get_object_or_404(Champion, pk=pk)

        if ChampionBasket.objects.filter(champion=champ, user=request.user) \
                and not SkinBasket.objects.filter(champion=champ, user=request.user):
            basket = ChampionBasket.objects.get(champion=champ, user=request.user)
            method = basket.method
            if method == 'rp':
                request.user.add_rp(champ.price_rp)
            else:
                request.user.add_be(champ.price_be)
            basket.delete()

    if cat == 'skins':
        skin = get_object_or_404(Skin, pk=pk)

        if SkinBasket.objects.filter(skin=skin, user=request.user):
            request.user.add_rp(skin.price_rp)
            SkinBasket.objects.get(skin=skin, user=request.user).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



