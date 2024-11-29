
# from django.contrib.auth.models import User
from ast import mod
from users.models import User
from django.db import models
from django.conf import settings
from categories.models import Category


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('sold', 'Sold')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=20,blank=True,null=True)
    # image = models.ImageField(upload_to='listing_images/', null=True, blank=True)
    
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"${self.id} ${self.title}" 
    
   


