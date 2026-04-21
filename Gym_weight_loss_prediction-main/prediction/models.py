"""
Models for the Gym Weight Loss Prediction app.
Stores prediction history and user input data.
"""
from django.db import models
from django.contrib.auth.models import User


class PredictionRecord(models.Model):
    """Model to store weight loss prediction records."""
    
    GENDER_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]
    
    # User who made the prediction (optional for anonymous users)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='predictions'
    )
    
    # Input features
    age = models.IntegerField(help_text="Age in years")
    gender = models.IntegerField(choices=GENDER_CHOICES, help_text="Gender (Male/Female)")
    height_cm = models.FloatField(help_text="Height in centimeters")
    weight_kg = models.FloatField(help_text="Weight in kilograms")
    workout_hours_per_week = models.FloatField(help_text="Workout hours per week")
    daily_calorie_intake = models.FloatField(help_text="Daily calorie intake")
    sleep_hours = models.FloatField(help_text="Sleep hours per day")
    
    # Prediction result
    predicted_weight_loss = models.FloatField(
        help_text="Predicted weight loss in kg",
        null=True, blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prediction Record'
        verbose_name_plural = 'Prediction Records'
    
    def __str__(self):
        return (
            f"Prediction #{self.pk} - Age: {self.age}, "
            f"Weight: {self.weight_kg}kg -> "
            f"Loss: {self.predicted_weight_loss}kg"
        )
    
    @property
    def bmi(self):
        """Calculate BMI from height and weight."""
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 1)
    
    @property
    def gender_display(self):
        """Return gender as string."""
        return 'Male' if self.gender == 1 else 'Female'
