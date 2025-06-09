# from django.shortcuts import render

# Create your views here.
# def orders(request):
#     return render(request, 'orders/orders.html')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, AssignedProduct
from products.models import Product
from django.contrib import messages
from django.http import JsonResponse


def create_order(request):
    product = Product.objects.first()
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        quantity = int(request.POST.get('quantity'))
        house_street = request.POST.get('house_street', '').strip()
        apartment = request.POST.get('apartment', '').strip()
        governorate = request.POST.get('governorate', '').strip()
        total = product.price * quantity
        shipping_address = f"{house_street}, {apartment}, {governorate}".strip(', ')

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            phone_number=phone,
            total_amount=total,
            status='pending',
            payment_status='unpaid',
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
        
        product.stock_quantity -= quantity
        product.save()
        
        messages.success(request, "Order placed successfully")
        request.session['order_message'] = "Order placed successfully"
        return redirect('products')

    return render(request, 'orders/orders.html', {'product': product})

def user_orders(request):
    current_orders = Order.objects.filter(
        user=request.user, status__in=['pending', 'processing']
    ).prefetch_related('orderitem_set__product').order_by('-order_date')

    previous_orders = Order.objects.filter(
        user=request.user, status='completed'
    ).prefetch_related('orderitem_set__product').order_by('-order_date')
    return render(request, 'orders/user_orders.html', {
        'current_orders': current_orders,
        'previous_orders': previous_orders,
        'product': Product.objects.first()
        })
    
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status not in ['completed', 'cancelled']:
        order.status = 'cancelled'
        order.save()
    return redirect('user_orders')