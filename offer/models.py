from django.db import models
from adminpage.models import Category,Product
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiry_time = models.DateTimeField(default=timezone.now)  # Default value is the current time


#using signal when a product offer is deleled it also trigger the price adjusted in varient to False
@receiver(post_delete, sender=ProductOffer)
def update_variant_price_adjusted(sender, instance, **kwargs):
    # Get related variants and set price_adjusted to False
    variants = instance.product.variants.filter(price_adjusted=True)
    for variant in variants:
        variant.price += instance.discount_amount
        variant.price_adjusted = False
        variant.save()



