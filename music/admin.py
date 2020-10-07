from django.contrib import admin
from .models import Song, Comment, Like

admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Like)
