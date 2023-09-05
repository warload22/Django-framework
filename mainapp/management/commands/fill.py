import json
from django.conf import settings
from django.core.management.base import BaseCommand
from authapp.models import Player
from mainapp.models import Champion, CollectionCategory, Skin, Icon

from lootapp.models import Material


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', 'r') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')
        champions = load_from_json('champions')
        skins = load_from_json('skins')
        icons = load_from_json('icons')
        loot = load_from_json('materials')

        CollectionCategory.objects.all().delete()
        for category in categories:
            CollectionCategory.objects.create(**category)

        Champion.objects.all().delete()
        for champion in champions:
            category_item = CollectionCategory.objects.get(name='champions')
            champion['category'] = category_item
            Champion.objects.create(**champion)

        Skin.objects.all().delete()
        for skin in skins:
            category_item = CollectionCategory.objects.get(name='skins')
            skin['category'] = category_item
            champion_name = skin['champion']
            champion_item = Champion.objects.get(name=champion_name)
            skin['champion'] = champion_item
            Skin.objects.create(**skin)

        Icon.objects.all().delete()
        for icon in icons:
            Icon.objects.create(**icon)

        Material.objects.all().delete()
        for material in loot:
            Material.objects.create(**material)

        try:
            Player.objects.get(username='django').delete()
        except:
            pass

        try:
            Player.objects.get(nickname='Django').delete()
        except:
            pass

        Player.objects.create_superuser(username='django', password='geekbrains', nickname='Django',
                                        age=18, email='django@gb.local')
        Player.objects.get(username='django').add_rp(100000)
        Player.objects.get(username='django').add_be(100000)