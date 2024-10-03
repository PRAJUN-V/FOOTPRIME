from django.db import models
from django.contrib.auth.models import User
from adminpage.models import Product, ProductVariant,Payment
from user_profile.models import UserAddress, UserMobile
from django.utils import timezone

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a user can have a cart
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other cart-related fields as needed

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=8)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    variant_stock_quantity = models.PositiveIntegerField(default=0)
    # Add other cart item-related fields as needed


class OrderDetails(models.Model):
    ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Refund', 'Refund'),
    ('Replacement', 'Replacement'),
    ('Return', 'Return'), 
]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    user_mobile = models.ForeignKey('user_profile.UserMobile', on_delete=models.SET_NULL, null=True, blank=True)
    user_address = models.TextField()

    # Fields related to each product in the order
    product = models.ForeignKey('adminpage.Product', on_delete=models.CASCADE,blank=True)
    product_variant = models.ForeignKey('adminpage.ProductVariant', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    # Add other fields related to order details as needed
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
