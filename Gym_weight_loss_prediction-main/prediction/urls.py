"""
URL patterns for the Prediction app.
Maps URLs to their corresponding views.
"""
from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    # Page routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('predict/', views.predict, name='predict'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API routes
    path('api/predict/', views.api_predict, name='api_predict'),
]
