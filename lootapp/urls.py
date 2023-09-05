from django.urls import path
import lootapp.views as lootapp

app_name = 'lootapp'

urlpatterns = [
    path('', lootapp.loot, name='index'),
    path('materials/', lootapp.loot, name='materials'),
    path('<str:name>/', lootapp.loot, name='category'),
]