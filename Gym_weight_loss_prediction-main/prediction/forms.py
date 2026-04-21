"""
Forms for the Gym Weight Loss Prediction app.
Handles user input validation for prediction requests.
"""
from django import forms
from .models import PredictionRecord


class PredictionForm(forms.Form):
    """Form for collecting user input for weight loss prediction."""
    
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        (1, 'Male'),
        (0, 'Female'),
    ]
    
    age = forms.IntegerField(
        min_value=15,
        max_value=80,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age',
            'id': 'age',
        }),
        help_text='Age between 15 and 80 years'
    )
    
    gender = forms.IntegerField(
        widget=forms.Select(
            choices=GENDER_CHOICES,
            attrs={
                'class': 'form-select',
                'id': 'gender',
            }
        ),
        help_text='Select your gender'
    )
    
    height_cm = forms.FloatField(
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter height in cm',
            'id': 'height_cm',
            'step': '0.1',
        }),
        help_text='Height in centimeters (100-250)'
    )
    
    weight_kg = forms.FloatField(
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter weight in kg',
            'id': 'weight_kg',
            'step': '0.1',
        }),
        help_text='Weight in kilograms (30-200)'
    )
    
    workout_hours_per_week = forms.FloatField(
        min_value=0,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hours per week',
            'id': 'workout_hours',
            'step': '0.5',
        }),
        help_text='Workout hours per week (0-30)'
    )
    
    daily_calorie_intake = forms.FloatField(
        min_value=800,
        max_value=5000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Daily calories',
            'id': 'calories',
            'step': '50',
        }),
        help_text='Daily calorie intake (800-5000)'
    )
    
    sleep_hours = forms.FloatField(
        min_value=3,
        max_value=12,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hours of sleep',
            'id': 'sleep_hours',
            'step': '0.5',
        }),
        help_text='Sleep hours per day (3-12)'
    )
    
    def clean_age(self):
        """Validate age field."""
        age = self.cleaned_data.get('age')
        if age and (age < 15 or age > 80):
            raise forms.ValidationError('Age must be between 15 and 80.')
        return age
    
    def clean_weight_kg(self):
        """Validate weight field."""
        weight = self.cleaned_data.get('weight_kg')
        if weight and weight <= 0:
            raise forms.ValidationError('Weight must be a positive number.')
        return weight
    
    def clean_height_cm(self):
        """Validate height field."""
        height = self.cleaned_data.get('height_cm')
        if height and height <= 0:
            raise forms.ValidationError('Height must be a positive number.')
        return height
