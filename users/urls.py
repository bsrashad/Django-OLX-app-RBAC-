from django.urls import path , include
from .views import RegisterView, LoginView ,UserProductListView
urlpatterns = [
    path('register',RegisterView.as_view()),
     path('login',LoginView.as_view()),
     path('<int:user_id>/products',UserProductListView.as_view()),
    path('favorite/',include('favorites.urls'))

   
]