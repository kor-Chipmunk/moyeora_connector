import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    path('auth/', include('user.urls')),
    path('introduce/', include('introduce.urls')),
    path('music/', include('music.urls')),
]
