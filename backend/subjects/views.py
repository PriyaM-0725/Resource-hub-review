from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subject
from .serializers import SubjectSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    user = request.user

    subjects = Subject.objects.filter(
        branch=user.branch,
        regulation=user.regulation
    )

    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)