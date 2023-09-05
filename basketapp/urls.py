from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('add/<str:cat>/<int:pk>/<str:method>/', basketapp.add, name='add'),
    path('remove/<str:cat>/<int:pk>/', basketapp.remove, name='remove')
]