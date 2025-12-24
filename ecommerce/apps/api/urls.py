from django.urls import path
from . import views

urlpatterns = [
    # On using Classed Based Views
    path("products/", views.ProductListCreateApiView.as_view()),
    # path("products/create/", views.ProductCreateApiView.as_view()),
    path("products/info/", views.ProductInfoListApiView.as_view()),
    path(
        "products/<int:product_id>/",
        views.ProductRetrieveUpdateDestroyApiView.as_view(),
    ),
    path("orders/", views.OrderListApiView.as_view()),
    path("user-orders/", views.UserOrderListApiView.as_view(), name="user-orders"),
    # On using Function Based Views
    # path("products/", views.product_list),
    # path("products/info/", views.product_info),
    # path("products/<int:pk>/", views.product_detail),
    # path("orders/", views.order_list),
]
