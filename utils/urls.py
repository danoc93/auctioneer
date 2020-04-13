from django.urls import path
from utils.views.HealthCheckView import HealthCheckView


urlpatterns = [
    path('health-check', HealthCheckView.as_view()),
]
