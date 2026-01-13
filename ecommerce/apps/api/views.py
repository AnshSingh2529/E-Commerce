from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

# ViewSets
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from silk.profiling.profiler import silk_profile

from apps.api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from apps.api.models import Order, Product
from apps.api.serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    OrderCreateSerializer,
)

# Classed based Views


class ProductListCreateApiView(generics.ListCreateAPIView):
    """Class-based view for listing and creating products."""

    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    # filterset_fields = ["name", "price"]
    filterset_class = ProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
        InStockFilterBackend,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 5

    """Customising permission to allow only authenticated users to create products,
    while allowing anyone to view the list of products.
    """

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class OrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related(
#         "items__product",
#     )
#     serializer_class = OrderSerializer


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

    # Generic Views + Mixins

    # class ProductListApiView(
    #     mixins.ListModelMixin,
    #     generics.GenericAPIView,
    # ):
    #     queryset = Product.objects.all()
    #     serializer_class = ProductSerializer
    #     # permission_classes = [IsAuthenticated]

    #     def get(self, request, *args, **kwargs):
    #         return self.list(request, *args, **kwargs)

    # class ProductDetailApiView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    #     queryset = Product.objects.all()
    #     serializer_class = ProductSerializer
    #     # permission_classes = [IsAuthenticated]

    #     def get(self, request, *args, **kwargs):
    #         return self.retrieve(request, *args, **kwargs)

    # """
    # Deprecated Code: ProductCreateApiView
    # """
    # # class ProductCreateApiView(generics.CreateAPIView):
    # #     model = Product
    # #     serializer_class = ProductSerializer

    #     # def create(self, request, *args, **kwargs):
    #     #     print("Creating a new product with data:", request.data)
    #     #     return super().create(request, *args, **kwargs)

    # class OrderListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    #     queryset = Order.objects.prefetch_related(
    #         "items__product",
    #     )
    #     serializer_class = OrderSerializer
    #     # permission_classes = [IsAuthenticated]

    #     def get(self, request, *args, **kwargs):
    #         return self.list(request, *args, **kwargs)

    # class UserOrderListApiView(mixins.ListModelMixin, generics.GenericAPIView):
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


# class ProductInfoListApiView(mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = ProductInfoSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Product.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()

#         data = {
#             "products": queryset,
#             "count": len(queryset),
#             "max_price": queryset.aggregate(max_price=Max("price"))["max_price"],
#         }
#         serializer = self.get_serializer(data)
#         return Response(serializer.data)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


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


# Views For Orders using ViewSets


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(
        detail=False,
        methods=["get"],
        url_path="user-orders",
        permission_classes=[IsAuthenticated],
    )
    def user_order(self, request):
        self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)
