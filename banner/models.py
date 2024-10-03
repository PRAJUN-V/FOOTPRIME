from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/banner_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title