from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    
class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    price = models.IntegerField()
    quantity = models.IntegerField()
    price_adjusted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.product.title} - {self.size}"

    

class multipleImage(models.Model):
    product=models.ForeignKey("adminpage.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)

    def __str__(self) -> str:
        return self.product.title


class Payment(models.Model):
    PAYMENT_TYPES = [
        ('COD', 'Cash on Delivery'),
        ('WALLET', 'Wallet'),
        ('Paypal', 'Paypal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    # Add other fields as needed, such as payment status, transaction ID, etc.

    