from django.contrib import admin

# Register your models here.

from .models import Product,Category,multipleImage,ProductVariant,Payment,Brand

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(multipleImage)
admin.site.register(ProductVariant)
admin.site.register(Payment)
admin.site.register(Brand)