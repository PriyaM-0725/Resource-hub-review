from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.db.models import Q
from .models import Resource, Bookmark, Rating, DownloadLog
from .serializers import ResourceSerializer, BookmarkSerializer, RatingSerializer


# 🔹 GET RESOURCES (FILTERED - personalized)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resources(request):
    user = request.user

    resources = Resource.objects.filter(
        branch=user.branch,
        year=user.year,
        regulation=user.regulation
    )

    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)


# 🔥 NEW: GET ALL RESOURCES (FOR DASHBOARD)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_resources(request):
    category = request.GET.get('type')

    resources = Resource.objects.all().order_by('-created_at')

    if category and category.lower() != "all":
        resources = resources.filter(type__iexact=category)

    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)


# 🔹 UPLOAD RESOURCE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resource(request):
    user = request.user

    serializer = ResourceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(
            uploaded_by=user,
            branch=user.branch,
            year=user.year,
            regulation=user.regulation
        )
        return Response(
            {"message": "Resource uploaded successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 ADD BOOKMARK
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bookmark(request):
    user = request.user
    resource_id = request.data.get('resource')

    if not resource_id:
        return Response({"error": "Resource ID required"}, status=400)

    bookmark, created = Bookmark.objects.get_or_create(
        user=user,
        resource_id=resource_id
    )

    if created:
        return Response({"message": "Bookmarked successfully"})
    else:
        return Response({"message": "Already bookmarked"})


# 🔹 GET BOOKMARKS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookmarks(request):
    user = request.user

    bookmarks = Bookmark.objects.filter(user=user)
    serializer = BookmarkSerializer(bookmarks, many=True)

    return Response(serializer.data)


# ⭐ RATE RESOURCE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_resource(request):
    user = request.user
    resource_id = request.data.get('resource')
    rating_value = request.data.get('rating')

    if not resource_id or not rating_value:
        return Response({"error": "resource and rating required"}, status=400)

    Rating.objects.update_or_create(
        user=user,
        resource_id=resource_id,
        defaults={'rating': rating_value}
    )

    return Response({"message": "Rating submitted"})


# 📥 DOWNLOAD RESOURCE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download_resource(request, resource_id):
    user = request.user

    try:
        resource = Resource.objects.get(id=resource_id)
    except Resource.DoesNotExist:
        return Response({"error": "Resource not found"}, status=404)

    resource.downloads_count += 1
    resource.save()

    DownloadLog.objects.create(user=user, resource=resource)

    return Response({
        "message": "Download recorded",
        "file_url": resource.file.url
    })


# 🔥 TRENDING RESOURCES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending_resources(request):
    resources = Resource.objects.all().order_by('-downloads_count')[:10]
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_resources(request):
    query = request.GET.get('q', '')

    resources = Resource.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    ).order_by('-created_at')

    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)