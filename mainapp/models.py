from django.db import models


class CollectionCategory(models.Model):
    name = models.CharField(verbose_name='name', max_length=32, unique=True)
    image = models.ImageField(verbose_name='loot image', blank=True)

    def __str__(self):
        return self.name


class Champion(models.Model):
    category = models.ForeignKey(CollectionCategory, on_delete=models.CASCADE, verbose_name='category')
    name = models.CharField(verbose_name='name', max_length=32, unique=True)
    image = models.ImageField(upload_to='champions', blank=True)
    price_rp = models.PositiveBigIntegerField(verbose_name='price rp')
    price_be = models.PositiveBigIntegerField(verbose_name='price blue essence')
    role = models.CharField(verbose_name='role', max_length=16)
    role_b = models.CharField(verbose_name='second role', max_length=16, blank=True)

    def __str__(self):
        return self.name


class Icon(models.Model):
    name = models.CharField(verbose_name='name', unique=True, max_length=32)
    image = models.ImageField(verbose_name='image')

    def __str__(self):
        return self.name


class Skin(models.Model):
    category = models.ForeignKey(CollectionCategory, on_delete=models.CASCADE, verbose_name='category')
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, verbose_name='champion')
    name = models.CharField(verbose_name='name', max_length=32, unique=True)
    image = models.ImageField(upload_to='skins', blank=True)
    price_rp = models.PositiveBigIntegerField(verbose_name='price_rp')
    division = models.CharField(verbose_name='division', max_length=16, blank=True)

    def __str__(self):
        return self.name


