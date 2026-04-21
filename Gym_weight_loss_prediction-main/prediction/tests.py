"""
Tests for the Gym Weight Loss Prediction app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import PredictionRecord


class PredictionModelTest(TestCase):
    """Test cases for the PredictionRecord model."""
    
    def setUp(self):
        """Set up test data."""
        self.record = PredictionRecord.objects.create(
            age=25,
            gender=1,
            height_cm=175,
            weight_kg=85,
            workout_hours_per_week=5,
            daily_calorie_intake=2200,
            sleep_hours=7,
            predicted_weight_loss=3.2,
        )
    
    def test_record_creation(self):
        """Test that a prediction record is created correctly."""
        self.assertEqual(self.record.age, 25)
        self.assertEqual(self.record.gender, 1)
        self.assertEqual(self.record.predicted_weight_loss, 3.2)
    
    def test_bmi_calculation(self):
        """Test BMI property calculation."""
        expected_bmi = round(85 / (1.75 ** 2), 1)
        self.assertEqual(self.record.bmi, expected_bmi)
    
    def test_gender_display(self):
        """Test gender display property."""
        self.assertEqual(self.record.gender_display, 'Male')
    
    def test_str_representation(self):
        """Test string representation."""
        self.assertIn('Prediction #', str(self.record))


class ViewsTest(TestCase):
    """Test cases for the views."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_home_page(self):
        """Test home page loads correctly."""
        response = self.client.get(reverse('prediction:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prediction/home.html')
    
    def test_about_page(self):
        """Test about page loads correctly."""
        response = self.client.get(reverse('prediction:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prediction/about.html')
    
    def test_predict_page_get(self):
        """Test prediction form page loads correctly."""
        response = self.client.get(reverse('prediction:predict'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prediction/predict.html')
    
    def test_dashboard_page(self):
        """Test dashboard page loads correctly."""
        response = self.client.get(reverse('prediction:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prediction/dashboard.html')
