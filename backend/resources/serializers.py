from rest_framework import serializers
from django.db.models import Avg
from .models import Resource, Bookmark, Rating
from subjects.models import Subject


# 🔹 RESOURCE SERIALIZER
class ResourceSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.ReadOnlyField(source='uploaded_by.username')
    average_rating = serializers.SerializerMethodField()

    # accept subject as string input
    subject = serializers.CharField(write_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Resource
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'branch', 'year', 'regulation']

    def get_average_rating(self, obj):
        avg = Rating.objects.filter(resource=obj).aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg else 0

    def create(self, validated_data):
        subject_name = validated_data.pop('subject')

        # 🔥 FIXED LOGIC (NO get_or_create WITH __iexact)
        subject = Subject.objects.filter(name__iexact=subject_name).first()

        if not subject:
            # ⚠️ IMPORTANT: add required fields (like semester)
            subject = Subject.objects.create(
                name=subject_name,
                semester=1   # 🔥 CHANGE THIS if needed
            )

        validated_data['subject'] = subject
        return super().create(validated_data)


# 🔹 BOOKMARK SERIALIZER
class BookmarkSerializer(serializers.ModelSerializer):
    resource_details = ResourceSerializer(source='resource', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'resource', 'resource_details']
        read_only_fields = ['user']


# 🔹 RATING SERIALIZER
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']