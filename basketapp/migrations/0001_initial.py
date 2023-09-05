# Generated by Django 3.2.8 on 2022-02-21 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.champion')),
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.skin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skin_basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=2, verbose_name='payment method')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.champion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champ_basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]