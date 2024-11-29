from django.urls import path , include
from .views import ProductDetailAPIView,ProductListCreateAPIView,ProductStatusUpdateView
from . import views
urlpatterns = [
    path('',ProductListCreateAPIView.as_view()),
    path('<int:pk>',ProductDetailAPIView.as_view()),
    path('updatestatus/<int:pk>',ProductStatusUpdateView.as_view()),
#    path('seller/products/', views.SellerProductListAPIView.as_view(), name='seller-product-list'),
    path('seller/', views.SellerProductCreateAPIView.as_view(), name='seller-product-create'),
    path('seller/<int:pk>/', views.SellerProductUpdateDeleteAPIView.as_view(), name='seller-product-update-delete'),
    path('admin/', views.AdminProductListAPIView.as_view(), name='admin-product-list'),
    path('admin /<int:pk>/', views.AdminProductDetailAPIView.as_view(), name='admin-product-detail'),
    path('admin/products/<int:pk>/approve/', views.AdminProductApproveAPIView.as_view(), name='admin-product-approve'),
    path('admin/products/<int:pk>/', views.AdminProductDeleteAPIView.as_view(), name='admin-product-delete'),
]