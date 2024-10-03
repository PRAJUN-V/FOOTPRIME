from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.home, name='home'),
    path('paypal_return/', views.paypal_return, name='paypal_return'),
    path('paypal_cancel/', views.paypal_cancel, name='paypal_cancel'),
]