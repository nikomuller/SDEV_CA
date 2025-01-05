from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('set/', views.SetCartItemView.as_view(), name='cart_set'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<uuid:product_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<uuid:product_id>/', views.full_remove, name='full_remove'),
    path('thanks/<uuid:order_id>/', views.ThankYouView.as_view(), name='thanks')
]
