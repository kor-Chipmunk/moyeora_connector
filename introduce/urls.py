from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('questions', views.get_questions),
    path('questions', views.post_questions),
    path('questions/<int:question_id>', views.get_question),
    path('questions/<int:question_id>', views.put_questions),
    path('questions/<int:question_id>', views.delete_questions),
])