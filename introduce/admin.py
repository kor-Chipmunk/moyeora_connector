from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at']
    list_filter = (
                    ('created_at', DateRangeFilter),
    )
    search_fields = ['content']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'user', 'question', 'created_at']
    list_filter = (
                    'question',
                    ('created_at', DateRangeFilter),
    )
    search_fields = ['content', 'user__nickname', 'question__content']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
