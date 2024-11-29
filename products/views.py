from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from throttling.custom_throttle import ScopedRateThrottle
# from orders.throttling.custom_throttle import ScopedRateThrottle
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly, IsSeller
from .decorators import role_required

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductListCreateAPIView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
   
    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        operation_description="Get a list of products",
    )
    def get(self,request):
      location=request.query_params.get('location',None)
      print(location)
      if location:
         productlist=Product.objects.filter(location__icontains=location)
         serializer=ProductSerializer(productlist,many=True)
         return Response(serializer.data,status=status.HTTP_200_OK)
      else:
         products=Product.objects.all()
         serializer=ProductSerializer(products,many=True)
         return Response(serializer.data,status=status.HTTP_200_OK)

    
class OrderCreateView(APIView):

    throttle_scope = 'another_scope'  # This scope should match the one defined in settings
    throttle_classes = [ScopedRateThrottle]
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: 'Bad Request'},
        operation_description="Create a new product",
    )
    def post(self,request):
       data=request.data
       serializer=ProductSerializer(data=data)
       if serializer.is_valid():
          serializer.save(seller=request.user)
          return Response(serializer.data,status=status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailAPIView(APIView):
   # permission_classes=[IsAuthenticatedOrReadOnly]
   
   def get_object(self,pk):
      return get_object_or_404(Product,pk=pk)
   
   
   @swagger_auto_schema(
        responses={200: ProductSerializer},
        operation_description="Retrieve a product by ID",
    )
   @role_required(['admin', 'seller'])
   def get(self,request,pk):
      product=self.get_object(pk)
      serializer=ProductSerializer(product)
      return Response(serializer.data,status=status.HTTP_200_OK)
   
   @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        operation_description="Update a product by ID",
    )
   def put(self,request,pk):
      product=self.get_object(pk)
      print(f"${product.seller} ")
      if product.seller != request.user:
         return Response({'error':'You can only update your own product'},status=status.HTTP_403_FORBIDDEN)
      data=request.data
      serializer=ProductSerializer(instance=product,data=data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_200_OK)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   @swagger_auto_schema(
        responses={204: 'No Content', 403: 'Forbidden'},
        operation_description="Delete a product by ID",
    )
   def delete(self,request,pk):
      product=self.get_object(pk)
      if product.seller != request.user:
         return Response({'error':'You can only delete your own product'},status=status.HTTP_403_FORBIDDEN)
      product.delete()
      return Response({'message':'Product deleted'},status=status.HTTP_204_NO_CONTENT)
   
class ProductStatusUpdateView(APIView):

   def get_object(self,pk):
      return get_object_or_404(Product,pk=pk)
   
   def put(self,request,pk):
      product=self.get_object(pk)
      if product.seller != request.user:
         return Response({'error':'You can only update your own product'},status=status.HTTP_403_FORBIDDEN)
      product.status='sold'
      product.save()
      return Response({'data':"product status is updated"},status=status.HTTP_200_OK)
   
from rest_framework.permissions import IsAuthenticated

class SellerProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
class SellerProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsSeller]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerProductUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated,IsSeller]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        product.delete()
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.permissions import IsAdminUser

class AdminProductListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminProductDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminProductApproveAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.status = request.data.get('status', 'available')
        product.save()
        return Response({"detail": "Product status updated."}, status=status.HTTP_200_OK)

class AdminProductDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



    
