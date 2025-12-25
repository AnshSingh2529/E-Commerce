from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

urlpatterns = [
    # On using Classed Based Views
    path("products/", views.ProductListCreateApiView.as_view()),
    # path("products/create/", views.ProductCreateApiView.as_view()),
    path("products/info/", views.ProductInfoListApiView.as_view()),
    path(
        "products/<int:product_id>/",
        views.ProductRetrieveUpdateDestroyApiView.as_view(),
    ),
    # On using Function Based Views
    # path("products/", views.product_list),
    # path("products/info/", views.product_info),
    # path("products/<int:pk>/", views.product_detail),
    # path("orders/", views.order_list),
]

router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename="order")

urlpatterns += router.urls
