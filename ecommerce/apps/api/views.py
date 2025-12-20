from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Max
from silk.profiling.profiler import silk_profile

from apps.api.serializers import (
    ProductSerializer,
    OrderSerializer,
    ProductInfoSerializer,
)
from apps.api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

# Classed based Views


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminUser]


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        "items__product",
    )
    serializer_class = OrderSerializer


class ProductInfoListApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


# Function Based Views

# @api_view(["GET"])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)  # --> It is from the (Browsable Api)


# @api_view(["GET"])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# @silk_profile(name="order_list_view")
# @api_view(["GET"])
# def order_list(request):
#     orders = Order.objects.prefetch_related(
#         "items__product",
#     )
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)  # --> It is from the (Browsable Api)


# @api_view(["GET"])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer(
#         {
#             "products   ": products,
#             "count": len(products),
#             "max_price": products.aggregate(max_price=Max("price"))["max_price"],
#         }
#     )
#     return Response(serializer.data)
