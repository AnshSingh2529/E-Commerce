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
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

# Generic Views + Mixins


class ProductListApiView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetailApiView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.prefetch_related(
        "items__product",
    )
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserOrderListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.prefetch_related(
        "items__product",
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = super().get_queryset()
        user_qs = qs.filter(user=request.user)
        self.queryset = user_qs
        return self.list(request, *args, **kwargs)


class ProductInfoListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProductInfoSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = {
            "products": queryset,
            "count": len(queryset),
            "max_price": queryset.aggregate(max_price=Max("price"))["max_price"],
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Classed based Views


#  class ProductListApiView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # permission_classes = [IsAdminUser]


# class ProductDetailApiView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class OrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related(
#         "items__product",
#     )
#     serializer_class = OrderSerializer


# class ProductInfoListApiView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductInfoSerializer(
#             {
#                 "products": products,
#                 "count": len(products),
#                 "max_price": products.aggregate(max_price=Max("price"))["max_price"],
#             }
#         )
#         return Response(serializer.data)


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
