# coupons/models.py
from django.db import models
from django.contrib.auth.models import User


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    valid_from = models.DateTimeField(null=True)
    valid_to = models.DateTimeField(null=True)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    maximum_usage_count = models.PositiveIntegerField(default=5)
    minimum_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=300)  # Add this field
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, default=2000, null=True)
    def __str__(self):
        return self.code
    
class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'coupon']

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"
