from itertools import product
from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Order
from users.models import User
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    # user=serializers.SerializerMethodField()
    product =  serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    total_price = serializers.SerializerMethodField() 
    class Meta:
        model=Order
        fields = ['id', 'user', 'product', 'status','total_price']
        read_only_fields = ['id','user','created_at','updated_at', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price

    def create(self, validated_data):
        product=validated_data.get('product')
        print("********",product)

        if product.status != 'available':
            raise serializers.ValidationError("Product is already sold.")
        
        order=Order.objects.create(
            user=validated_data.get('user'),
            product=validated_data.get('product'),
            total_price=product.price,
            status=validated_data.get('status')
        )
        return order
    
    def get_user(self,obj):
        serializer=UserSerializer(obj.user)
        return serializer.data
