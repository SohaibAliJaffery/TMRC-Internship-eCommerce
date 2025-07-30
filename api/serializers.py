from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = (
      'id',
      'name',
      'description',
      'price',
      'stock',
    )

  def validate_price(self, value):
    if value < 0:
      raise serializers.ValidationError("Price must be a positive number.")
    return value


class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = ('product', 'quantity',)
  


class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True, read_only=True)


  class Meta:
    model = Order
    fields = (
      'order_id', 
      'created_at', 
      'user', 
      'status',
      'items',
    )