from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import Song, Comment, Like

class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'url', 'is_played', 'count_likes', 'count_comments', 'created_at', ]
    list_filter = ('is_played',
                   ('created_at', DateTimeRangeFilter),
                   )
    search_fields = ['user__nickname', 'title', 'url', ]
    ordering = ('is_played', 'id', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'song', 'count_likes', 'created_at',]
    list_filter = ('song',
                   ('created_at', DateTimeRangeFilter),
                   )
    search_fields = ['user__nickname', 'content', 'song_title', ]

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'song', 'created_at', ]
    list_filter = ('song',
                   ('created_at', DateTimeRangeFilter),
                   )
    search_fields = ['user__nickname', 'content', 'song_title', ]

admin.site.register(Song, SongAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)