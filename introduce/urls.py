from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('questions', views.create_list_questions),
    path('questions/<int:question_id>', views.retrieve_update_destory_question),

    path('answers', views.list_create_answers),
    path('answers/<int:answer_id>', views.get_answer),
])