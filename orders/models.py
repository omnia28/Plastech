from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    payment_choices = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=payment_choices, default='unpaid')
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
class AssignedProduct(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    unique_product_id = models.CharField(max_length=100, unique=True)
    result_url = models.URLField(blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now=True)