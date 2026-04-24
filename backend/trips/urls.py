from django.urls import path
from . import views

urlpatterns = [
    path('trips/', views.TripCreateView.as_view(), name='trip-create'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='trip-detail'),
    path('health/', views.health_check, name='health-check'),
]
