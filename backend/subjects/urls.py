from django.urls import path
from .views import get_subjects

urlpatterns = [
    path('', get_subjects),
]