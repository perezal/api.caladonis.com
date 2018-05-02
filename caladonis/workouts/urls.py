from django.urls import path

from . import views

app_name = 'workouts'
urlpatterns = [
    path('', views.WorkoutList.as_view(), name='index'),
    path('<int:pk>/', views.WorkoutEdit.as_view(), name='workout'),
    path('new/', views.WorkoutCreate.as_view(), name='create'),
]