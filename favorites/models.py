from django.db import models
# from django.contrib.auth.models import User
from products.models import Product
from users.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')        
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.name} - {self.product.title}"
