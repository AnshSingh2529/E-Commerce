from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]


admin.site.register(Order, OrderAdmin)
