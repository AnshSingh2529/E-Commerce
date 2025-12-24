import django_filters
from apps.api.models import Product
from rest_framework.filters import BaseFilterBackend



class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        #   fields = ("name", "price")
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["lt", "gt", "exact", "range"],
        }
