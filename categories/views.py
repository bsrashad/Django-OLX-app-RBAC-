from django.shortcuts import render
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
