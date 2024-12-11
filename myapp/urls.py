# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
 
    path('', views.fun),  # Your homepage view
    path('recommend/', views.get_recommendations),  # Your recommendation view
]
