from datetime import datetime, timedelta
import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(AbstractUser):
    nickname = models.CharField(max_length=16, unique=True, verbose_name='nickname')
    icon = models.ImageField(default='icons/Gromp.png', verbose_name='icon')
    age = models.PositiveSmallIntegerField(verbose_name='age', default=18)
    blue_essence = models.PositiveIntegerField(verbose_name='blue essence balance', default=0)
    rp = models.PositiveIntegerField(verbose_name='rp balance', default=0)
    is_active = models.BooleanField(verbose_name='is active', default=True)
    email = models.EmailField(verbose_name='email')
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activation_key_expires + timedelta(hours=48):
            return True
        return False

    def add_be(self, amount):
        self.blue_essence += amount
        self.save()

    def add_rp(self, amount):
        self.rp += amount
        self.save()

    def subtract_be(self, amount):
        self.blue_essence -= amount
        self.save()

    def subtract_rp(self, amount):
        self.rp -= amount
        self.save()


class PlayerProfile(models.Model):

    male = 'M'
    female = 'F'

    genders = (
        (male, 'Male'),
        (female, 'Female')
    )

    user = models.OneToOneField(Player, null=True, unique=True, on_delete=models.CASCADE, db_index=True)
    about_me = models.TextField(verbose_name='about me')
    gender = models.CharField(choices=genders, default=male, max_length=1, verbose_name='gender')

    @receiver(post_save, sender=Player)
    def create_player_profile(sender, instance, created, **kwargs):
        if created:
            PlayerProfile.objects.create(user=instance)

    @receiver(post_save, sender=Player)
    def update_player_profile(sender, instance, **kwargs):
        instance.playerprofile.save()
