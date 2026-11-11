from django.urls import path
from .views import register_user, login_user
from .views import register_user, login_user, get_profile
urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('profile/', get_profile),
]