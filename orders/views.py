from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from rest_framework.permissions import AllowAny
from .pagination import MyPageNumberPagination 
import asyncio
# Create your views here.
from throttling.custom_throttle import ScopedRateThrottle
class OrderCreateView(APIView):

    throttle_scope = 'another_scope'  # This scope should match the one defined in settings
    throttle_classes = [ScopedRateThrottle]
    
    @swagger_auto_schema(
        request_body=OrderSerializer,
        operation_description="Create a new order",
    )
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDisplayView(APIView):
    # permission_classes=[AllowAny]
    throttle_scope = 'my_view_scope'  # This scope should match the one defined in settings
    throttle_classes = [ScopedRateThrottle]
   

    def get(self,request,orderid,format=None):
        order=get_object_or_404(Order,pk=orderid)
        serializer=OrderSerializer(order)
        return Response(serializer.data)
   
    
# class OrderUserDisplayView(APIView):
#     pagination_class = MyPageNumberPagination 
#     def get(self,request,userid):
#         usersorder = Order.objects.filter(user_id=userid)
#         serializer = OrderSerializer(usersorder, many=True)
#         return Response(serializer.data)


class OrderUserDisplayView(APIView):
    pagination_class = MyPageNumberPagination
    
    def get(self, request, userid):
        # Filter orders by user ID
        usersorder = Order.objects.filter(user_id=userid)
        
        # Create an instance of the pagination class
        paginator = self.pagination_class()
        
        # Paginate the queryset
        page = paginator.paginate_queryset(usersorder, request)
        
        # Serialize the paginated data
        serializer = OrderSerializer(page, many=True)
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
