from cmath import pi
import pandas as pd
import json
from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

df=pd.read_csv("D:/software/ecommerce/backend/base/testdata.csv")
datadf = df.to_dict(orient='records')
print("datadf", datadf)
# print((datadf[0]))
# json_string = json.dumps(datadf) 
# print(json_string)

from base.models import Product
from .products import products
from rest_framework.response import Response
from .serializers import ProductSerializer

# JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# END
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    return JsonResponse('Hello from getRoutes', safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    products=Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    return Response(datadf)
    # return Response(serializers.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

