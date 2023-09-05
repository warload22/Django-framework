from django.urls import path
import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.OrderListView.as_view(), name='list'),
    path('create/', orderapp.OrderCreateView.as_view(), name='create'),
    path('read/<int:pk>/', orderapp.OrderDetailView.as_view(), name='read'),
    path('update/<int:pk>/', orderapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', orderapp.OrderDeleteView.as_view(), name='delete'),
    path('proceed/<int:pk>/', orderapp.order_sending_to_payment, name='proceed'),
    path('payment/<int:pk>/', orderapp.order_payment, name='payment'),
    path('material/price/<int:pk>/', orderapp.get_material_price, name='get_material_price')
]