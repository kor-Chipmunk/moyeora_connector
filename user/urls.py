from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserLoginAPIView, UserCreateAPIView

urlpatterns = format_suffix_patterns([
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register')
])