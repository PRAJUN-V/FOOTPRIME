from django.urls import path
from . import views

app_name = 'wishlist'
urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/<int:varient>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist_item/<int:wishlist_item_id>/', views.remove_wishlist_item, name='remove_wishlist_item'),
]