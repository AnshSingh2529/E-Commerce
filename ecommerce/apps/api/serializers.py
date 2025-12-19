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

class OrderSerializer(serializers.ModelSerializer):
    pass