from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('otp/', views.otp_verification, name='otp_verification'),
    path('product_details/<int:id>', views.product_details, name='product_details'),
    path('resent_otp/', views.resent_otp, name='resent_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password_otp_verification/', views.forgot_password_otp_verification, name='forgot_password_otp_verification'),
    path('product_details_varient/<int:id>/<int:varient>', views.product_details_varient, name='product_details_varient'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('change_password/', views.change_password, name='change_password'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('enquiry/', views.enquiry, name='enquiry'),
]