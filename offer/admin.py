from django.contrib import admin

# Register your models here.
from .models import CategoryOffer,ProductOffer

admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)

