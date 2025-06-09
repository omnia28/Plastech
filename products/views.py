from django.shortcuts import render
from .models import Product

# Create your views here.
def products(request):
    order_message = request.session.pop('order_message', None)
    product = Product.objects.all()
    return render(request, 'products/products.html', {'products': product, 'order_message': order_message})