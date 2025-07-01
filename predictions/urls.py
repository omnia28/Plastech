from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_sensor, name='select_sensor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.sensor_history, name='sensor_history'),
]
