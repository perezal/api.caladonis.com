from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('new/', views.AccountView.as_view(), name='index'),
]