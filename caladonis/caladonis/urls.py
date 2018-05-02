from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),
    path('accounts/', include('accounts.urls')),
    path('login/', views.obtain_auth_token),
]