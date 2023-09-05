from django.db import models
from django.conf import settings
from mainapp.models import Champion, Skin
from django.utils.functional import cached_property


class ChampionBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='champ_basket')
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    method = models.CharField(max_length=2, verbose_name='payment method')
    add_datetime = models.DateTimeField(verbose_name='time', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.champ_basket.select_related()

    def get_owned(self):
        return self.get_items_cached.values_list('champion', flat=True)

    @property
    def get_total_cost(self):
        rp = sum(list(map(lambda x: x.champion.price_rp, self.get_items_cached.filter(method='rp'))))
        be = sum(list(map(lambda x: x.champion.price_be, self.get_items_cached.filter(method='be'))))
        return [rp, be]


class SkinBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skin_basket')
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    add_datetime = models.DateTimeField(verbose_name='time', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.skin_basket.select_related()

    def get_owned(self):
        return self.get_items_cached.values_list('skin', flat=True)

    @staticmethod
    def get_division(skins, div):
        if skins:
            return skins.filter(skin__division=div)
        else:
            return []

    @property
    def get_total_cost(self):
        return sum(list(map(lambda x: x.skin.price_rp, self.get_items_cached)))
