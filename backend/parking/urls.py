from django.urls import path
from .views import (
    ParkingListCreateView,
    ParkingDetailView,
    ParkingStatsView
)

urlpatterns = [
    path('', ParkingListCreateView.as_view()),
    path('<int:pk>/', ParkingDetailView.as_view()),
    path('<int:pk>/stats/', ParkingStatsView.as_view()),
]