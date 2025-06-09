from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order, name='orders'),
    path('my_orders/', views.user_orders, name='user_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]