from django.urls import path
from . import views

app_name = 'user_profile'
urlpatterns = [
    path('', views.userProfile, name='user_profile'),
    path('user_address/', views.user_address, name='user_address'),
    path('add_user_address/', views.add_user_address, name='add_user_address'),
    path('add_user_mobile/', views.add_user_mobile, name='add_user_mobile'),
    path('add_user_firstname/', views.add_user_firstname, name='add_user_firstname'),
    path('add_user_lastname/', views.add_user_lastname, name='add_user_lastname'),
    path('edit_user_mobile/', views.edit_user_mobile, name='edit_user_mobile'),
    path('edit_user_firstname/', views.edit_user_firstname, name='edit_user_firstname'),
    path('edit_user_lastname/', views.edit_user_lastname, name='edit_user_lastname'),
    path('delete_user_address/<int:id>', views.delete_user_address, name='delete_user_address'),
    path('user_order/', views.user_order, name='user_order'),
    path('cancel_order/<int:id>', views.cancel_order, name='cancel_order'),
    path('refund_order/<int:id>', views.refund_order, name='refund_order'),
    path('replacement_order/<int:id>', views.replacement_order, name='replacement_order'),
    path('add_address_checkout/', views.add_address_checkout, name='add_address_checkout'),
    path('more_order_details/<int:id>', views.more_order_details, name='more_order_details'),
    path('invoice/<int:id>', views.invoice, name='invoice'),
]