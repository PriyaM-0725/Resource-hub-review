from django.urls import path
from .views import search_resources
from .views import (
    get_resources,
    all_resources,      # 🔥 NEW
    upload_resource,
    add_bookmark,
    get_bookmarks,
    rate_resource,
    download_resource,
    trending_resources
)

urlpatterns = [
    path('', get_resources),
    path('all/', all_resources),   # 🔥 IMPORTANT
    path('upload/', upload_resource),
    path('bookmark/', add_bookmark),
    path('bookmarks/', get_bookmarks),
    path('rate/', rate_resource),
    path('download/<int:resource_id>/', download_resource),
    path('trending/', trending_resources),
    path('search/', search_resources),
    
]