from django.db import models
from adminpage.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a user can have a wishlist
    products = models.ManyToManyField(Product, through='WishlistItem')
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other wishlist-related fields as needed

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(default=8)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    variant_stock_quantity = models.PositiveIntegerField(default=0)
    # You might adjust the fields based on your specific requirements for a wishlist item
    # For example, you may or may not need a price field in a wishlist item.


