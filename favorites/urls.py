from django.urls import path
from .views import UserFavoritesView ,AddFavoriteView,DeleteFavoriteView ,ProductFavoriteView

urlpatterns = [
    path('<int:user_id>', UserFavoritesView.as_view(), name='user-favorites'),
    path('add/<int:product_id>', AddFavoriteView.as_view(), name='add-favorite'),
    path('remove/<int:product_id>', DeleteFavoriteView.as_view(), name='add-favorite'),
    path('product/<int:product_id>', ProductFavoriteView.as_view(), name='add-favorite'),
    # path('products/<int:product_id>/favorites/remove/', RemoveFavoriteView.as_view(), name='remove-favorite'),
    # path('products/<int:product_id>/favorites/', ProductFavoritesView.as_view(), name='product-favorites'),
]
