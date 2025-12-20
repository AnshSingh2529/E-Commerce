from django.urls import path
from . import views

urlpatterns = [
    # On using Classed Based Views
    path("products/", views.ProductListApiView.as_view()),
    path("products/info/", views.ProductInfoListApiView.as_view()),
    path("products/<int:pk>/", views.ProductDetailApiView.as_view()),
    path("orders/", views.OrderListApiView.as_view()),
    
    # On using Function Based Views
    # path("products/", views.product_list),
    # path("products/info/", views.product_info),
    # path("products/<int:pk>/", views.product_detail),
    # path("orders/", views.order_list),
]
