from django.shortcuts import render
from rest_framework.views import APIView
from .models import Favorite
from products.models import Product
from .serializers import FavoriteSerializer
from products.serializers import ProductSerializer
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# Create your views here.

class UserFavoritesView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,user_id):
        userfavorites=Favorite.objects.filter(user_id=user_id)
        productlist=[favorite.product for favorite in userfavorites]
        serializer=ProductSerializer(productlist,many=True)
        return Response(serializer.data)

class AddFavoriteView(APIView):
    def post(self,request,product_id):
        user=request.user
        try:
            productseller=Product.objects.filter(seller=user)
            for product in productseller:
                if product.id == product_id:
                    return Response({"message":"this product is owned by you"})
            product=Product.objects.get(id=product_id)
            favoriteproduct , created=Favorite.objects.get_or_create(user=user,product=product)
            if created:
                return Response({"message":"this product is successfully added to favorites"})
            else:
                return Response({"message":"this product is already there in favorites"})
        except Product.DoesNotExist:
            return Response({"error":"Product Not Found"},status=status.HTTP_404_NOT_FOUND)
        

class DeleteFavoriteView(APIView):
    def delete(self,request,product_id):
        user=request.user
        try:
            fetchproduct=Favorite.objects.get(user=user,product_id=product_id)
            fetchproduct.delete()
            return Response({"message":"this product is successfully deleted from favorites"})
        except Favorite.DoesNotExist:
            return Response({"message":"this product does not exist  in favorites"})
        

class ProductFavoriteView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,product_id):
        favoriteproductlist=Favorite.objects.filter(product_id=product_id)
        userslist=[favorite.user for favorite in favoriteproductlist]
        serializer=UserSerializer(userslist,many=True)
        return Response(serializer.data)

        

        
