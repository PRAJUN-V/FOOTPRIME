from django.urls import path
from . import views

app_name = 'cart_management'
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/<int:varient>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/<int:product_id>/<int:varient>/', views.checkout, name='checkout'),
    path('order_confirmed/', views.order_confirmed, name='order_confirmed'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('quantity_add/<int:cart_item_id>/<int:product_id>/<int:size>/', views.quantity_add, name='quantity_add'),
    path('quantity_minus/<int:cart_item_id>/', views.quantity_minus, name='quantity_minus'),
    path('payment_page/', views.payment_page, name='payment_page'),     
]