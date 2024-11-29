from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializer
from categories.serializers import CategorySerializer
from users.models import User
from categories.models import Category
class ProductSerializer(serializers.ModelSerializer):
    # seller=UserSerializer(read_only=True)
    # category=CategorySerializer(read_only=True)
    # seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    seller = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  
    class Meta:
        model = Product
        fields = ['id', 'seller', 'title', 'description', 'price', 'status', 'category', 'created_at','location']
        read_only_fields = ['id', 'seller', 'created_at']
