from django.db import models

# Create your models here.
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30,unique=TRUE)
    password=models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    username=None

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]


    objects=UserManager()

    def __str__(self):
         return f"${self.id} ${self.name}" 

