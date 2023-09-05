from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.user_list, name='user_list'),
    path('users/read/<int:page>/', adminapp.user_list, name='user_page'),
    path('users/update/<int:pk>/', adminapp.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('users/detail/<int:pk>/', adminapp.UserDetailView.as_view(), name='user_detail'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.category_list, name='category_list'),
    path('categories/update/<int:pk>/', adminapp.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    path('champions/create/', adminapp.ChampionCreateView.as_view(), name='champion_create'),
    path('champions/read/', adminapp.ChampionListView.as_view(), name='champion_list'),
    path('champions/read/<int:page>/', adminapp.ChampionListView.as_view(), name='champion_page'),
    path('champions/update/<int:pk>/', adminapp.ChampionUpdateView.as_view(), name='champion_edit'),
    path('champions/delete/<int:pk>/', adminapp.ChampionDeleteView.as_view(), name='champion_delete'),
    path('champions/detail/<int:pk>/', adminapp.ChampionDetailView.as_view(), name='champion_detail'),

    path('skins/create/', adminapp.SkinCreateView.as_view(), name='skin_create'),
    path('skins/read/', adminapp.SkinListView.as_view(), name='skin_list'),
    path('skins/read/<int:page>/', adminapp.SkinListView.as_view(), name='skin_page'),
    path('skins/update/<int:pk>/', adminapp.SkinUpdateView.as_view(), name='skin_edit'),
    path('skins/delete/<int:pk>/', adminapp.SkinDeleteView.as_view(), name='skin_delete'),
    path('skins/detail/<int:pk>/', adminapp.SkinDetailView.as_view(), name='skin_detail')
]
