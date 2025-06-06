from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='productsImages/', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name