from cmath import pi
import pandas as pd
import json
from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


df=pd.read_csv("D:/software/ecommerce/backend/base/testdata.csv")
datadf = df.to_dict(orient='records')
print("datadf", datadf)
# print((datadf[0]))
# json_string = json.dumps(datadf) 
# print(json_string)

from base.models import Product
from .products import products
from rest_framework.response import Response
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

# JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# END
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    return JsonResponse('Hello from getRoutes', safe=False)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProducts(request):
    products=Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    # return Response(datadf)
    return Response(serializers.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

# @api_view(['GET'])
# def getProduct(request, pk):
#     product = Product.objects.get(_id=pk)
#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)


@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

