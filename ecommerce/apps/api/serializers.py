from .models import User, Order, Product, OrderItem
from rest_framework import serializers

"""
   Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into 'JSON', 'XML' or other content types, Serializers also provide deserialization , allowing parsed data to be  converted back into complex types, after first validating the incoming data
"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


"""
      #   read_only = () -> can only get the values from client but Not permission to update or create operations !!
      #   write_only = () -> can perform create and update operation
      #   required = () -> Normally an error will be raised if a field is not supplied
"""


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer() # For return the whole product info..
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="product.price")
    product_description = serializers.CharField(source="product.description")

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "product_description",
            "quantity",
            "item_subtotal"
        )


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(
        many=True, read_only=True
    )  # if you don't use the structure it will only provide the product ids and quantity only
    total_price = serializers.SerializerMethodField(method_name="total_order_price")

    def total_order_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "create_at",
            "status",
            "items",
            "total_price",
        )

class ProductInfoSerializer(serializers.Serializer):
    # get all product, count of products, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()