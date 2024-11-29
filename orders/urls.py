from django.urls import path
from .views import OrderCreateView,OrderDisplayView,OrderUserDisplayView

urlpatterns = [

    path('',OrderCreateView.as_view()),
    path('<int:orderid>',OrderDisplayView.as_view()),
    path('user/<int:userid>',OrderUserDisplayView.as_view())

]