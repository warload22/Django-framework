from django.db import models
from mainapp.models import Champion, Skin

from authapp.models import Player


class Material(models.Model):

    name = models.CharField(verbose_name='name', max_length=32, unique=True)
    image = models.ImageField(upload_to='loot', blank=True)
    price_rp = models.PositiveBigIntegerField(verbose_name='price rp', blank=True)
    is_purchasable = models.BooleanField(default=False)
    quantity = models.SmallIntegerField(default=1000, verbose_name='quantity')

    def __str__(self):
        return self.name


class ChampShard(models.Model):

    champ = models.ForeignKey(Champion, on_delete=models.CASCADE)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)

    @property
    def price_be_disenchant(self):
        return round(self.champ.price_be * 0.2, 0)

    @property
    def price_be_upgrade(self):
        return round(self.champ.price_be * 0.6, 0)


class SkinShard(models.Model):

    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)

    @property
    def price_oe_disenchant(self):
        if self.skin.price_oe:
            return round(self.skin.price_oe * 0.2, 0)

    @property
    def price_oe_upgrade(self):
        if self.skin.price_oe:
            return round(self.skin.price_oe * 0.75, 0)


class PurchasedMaterial(models.Model):

    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)
    opened = models.PositiveSmallIntegerField(null=False, default=0)

    @property
    def get_total_cost(self):
        return (self.quantity + self.opened) * self.material.price_rp
