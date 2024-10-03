"""
URL configuration for footprime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.conf import settings # new
from  django.conf.urls.static import static #new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('',include('home.urls',namespace='home')),
    path('adminpage/',include('adminpage.urls',namespace='adminpage')),
    path('user_profile/',include('user_profile.urls',namespace='user_profile')),
    path('cart_management/',include('cart_management.urls',namespace='cart_management')),
    path('wishlist/',include('wishlist.urls',namespace='wishlist')),
    path('coupon/',include('coupon.urls',namespace='coupon')),
    path('wallet/',include('wallet.urls',namespace='wallet')),
    path('payment/',include('payment.urls',namespace='payment')),
    path('banner/',include('banner.urls',namespace='banner')),
    path('offer/',include('offer.urls',namespace='offer')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
