import imp
from django.urls import path

from . import views

urlpatterns = [
    path('api/users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', views.getRoutes, name="routes"),
    path('api/products', views.getProducts, name="products"),
    path('api/product/<str:pk>', views.getProduct, name="product"),
]