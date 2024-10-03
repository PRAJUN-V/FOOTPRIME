from django.contrib import admin
from .models import Cart
from .models import OrderDetails,CartItem
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderDetails)