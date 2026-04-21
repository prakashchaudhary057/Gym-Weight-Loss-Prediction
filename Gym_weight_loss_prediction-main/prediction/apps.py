"""
App configuration for the prediction app.
"""
from django.apps import AppConfig


class PredictionConfig(AppConfig):
    """Configuration class for the Prediction app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    verbose_name = 'Weight Loss Prediction'
