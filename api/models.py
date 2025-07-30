import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  """
  Custom user model that extends the default Django user model.
  This can be used to add additional fields or methods in the future.
  """
  # Additional fields can be added here if needed
  pass

class Product(models.Model):
  """
  Model representing a product in the system.
  """
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField()
  image = models.ImageField(upload_to='products/', blank=True, null=True)
  
  
  #created_at = models.DateTimeField(auto_now_add=True)
  #updated_at = models.DateTimeField(auto_now=True)
  
  @property
  def in_stock(self):
    return self.stock > 0

  def __str__(self):
    return self.name


class Order(models.Model):
  class StatusChoices(models.TextChoices):
    PENDING ='Pending'
    CONFIRMED ='Confirmed'
    CANCELLED ='Cancelled'

  order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(
    max_length=10,
    choices=StatusChoices.choices,
    default=StatusChoices.PENDING
  )

  products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

  def __str__(self):
    return f"Order {self.order_id} by {self.user.username} - {self.status}"
  

class OrderItem(models.Model):
  order = models.ForeignKey(
    Order, 
    on_delete=models.CASCADE,
    related_name='items'
  )
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()

  @property
  def item_subtotal(self):
    return self.product.price * self.quantity
  
  def __str__(self):
    return f"{self.quantity} x {self.product.name} (Order {self.order.order_id})"