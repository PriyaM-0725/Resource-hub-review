from django.contrib import admin
from .models import Resource
from .models import Bookmark
from .models import Rating
from .models import DownloadLog
admin.site.register(DownloadLog)
admin.site.register(Rating)
admin.site.register(Bookmark)
admin.site.register(Resource)