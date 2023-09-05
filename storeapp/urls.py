from django.urls import path
import storeapp.views as storeapp

app_name = 'storeapp'

urlpatterns = [
    path('', storeapp.store, name='index'),
    path('<str:name>/', storeapp.store, name='category'),
    path('<str:name>/<str:role>/', storeapp.store, name='champs'),
    path('add/<str:cat>/<int:pk>/', storeapp.add, name='add'),
]