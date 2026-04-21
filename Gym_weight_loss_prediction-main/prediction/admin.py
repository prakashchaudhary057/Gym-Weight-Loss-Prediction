"""
Admin configuration for the Prediction app.
Registers models with the Django admin panel.
"""
from django.contrib import admin
from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    """Admin configuration for PredictionRecord model."""
    
    list_display = [
        'id', 'age', 'gender_display', 'weight_kg', 
        'workout_hours_per_week', 'predicted_weight_loss', 'created_at'
    ]
    list_filter = ['gender', 'created_at']
    search_fields = ['age', 'weight_kg']
    readonly_fields = ['predicted_weight_loss', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'age', 'gender', 'height_cm', 'weight_kg')
        }),
        ('Lifestyle Data', {
            'fields': ('workout_hours_per_week', 'daily_calorie_intake', 'sleep_hours')
        }),
        ('Prediction Result', {
            'fields': ('predicted_weight_loss',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def gender_display(self, obj):
        """Display gender as readable string."""
        return obj.gender_display
    gender_display.short_description = 'Gender'
