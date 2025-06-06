from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, AssignedProduct
import random

def generate_unique_product_id():
    while True:
        uid = f"Plas-{random.randint(1000, 999999)}"
        if not AssignedProduct.objects.filter(unique_product_id=uid).exists():
            return uid

@receiver(post_save, sender=OrderItem)
def create_assigned_products(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.quantity):
            AssignedProduct.objects.create(
                order_item=instance,
                unique_product_id=generate_unique_product_id()
            )
