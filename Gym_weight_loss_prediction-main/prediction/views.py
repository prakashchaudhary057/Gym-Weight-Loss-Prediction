"""
Views for the Gym Weight Loss Prediction app.
Handles page rendering, form processing, and ML model predictions.
"""
import os
import json
import numpy as np
import pandas as pd
import joblib
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from .forms import PredictionForm
from .models import PredictionRecord


def load_model():
    """
    Load the trained ML model and scaler from disk.
    Returns tuple of (model, scaler) or (None, None) if loading fails.
    """
    try:
        model_path = settings.ML_MODEL_PATH
        scaler_path = settings.ML_SCALER_PATH
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
        else:
            print(f"Model files not found at {model_path} or {scaler_path}")
            return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


def home(request):
    """Render the home page with project overview."""
    # Get some stats for the home page
    total_predictions = PredictionRecord.objects.count()
    context = {
        'total_predictions': total_predictions,
        'page_title': 'Home',
    }
    return render(request, 'prediction/home.html', context)


def about(request):
    """Render the about page with project objectives and methodology."""
    context = {
        'page_title': 'About',
    }
    return render(request, 'prediction/about.html', context)


def predict(request):
    """
    Handle the prediction form.
    GET: Display the prediction form.
    POST: Process form data, run ML prediction, and display results.
    """
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned form data
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            height_cm = form.cleaned_data['height_cm']
            weight_kg = form.cleaned_data['weight_kg']
            workout_hours = form.cleaned_data['workout_hours_per_week']
            calories = form.cleaned_data['daily_calorie_intake']
            sleep_hours = form.cleaned_data['sleep_hours']
            
            # Load the trained model
            model, scaler = load_model()
            
            if model is not None and scaler is not None:
                try:
                    # Prepare input data as numpy array
                    input_data = np.array([[
                        age, gender, height_cm, weight_kg,
                        workout_hours, calories, sleep_hours
                    ]])
                    
                    # Scale the input data
                    input_scaled = scaler.transform(input_data)
                    
                    # Make prediction
                    prediction = model.predict(input_scaled)[0]
                    predicted_weight_loss = round(float(prediction), 2)
                    
                    # Ensure prediction is non-negative
                    predicted_weight_loss = max(0, predicted_weight_loss)
                    
                    # Save prediction record to database
                    record = PredictionRecord.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        age=age,
                        gender=gender,
                        height_cm=height_cm,
                        weight_kg=weight_kg,
                        workout_hours_per_week=workout_hours,
                        daily_calorie_intake=calories,
                        sleep_hours=sleep_hours,
                        predicted_weight_loss=predicted_weight_loss,
                    )
                    
                    # Generate interpretation
                    interpretation = get_interpretation(predicted_weight_loss, workout_hours, calories)
                    
                    # Calculate BMI
                    height_m = height_cm / 100
                    bmi = round(weight_kg / (height_m ** 2), 1)
                    bmi_category = get_bmi_category(bmi)
                    
                    context = {
                        'prediction': predicted_weight_loss,
                        'interpretation': interpretation,
                        'bmi': bmi,
                        'bmi_category': bmi_category,
                        'input_data': {
                            'age': age,
                            'gender': 'Male' if gender == 1 else 'Female',
                            'height_cm': height_cm,
                            'weight_kg': weight_kg,
                            'workout_hours': workout_hours,
                            'calories': calories,
                            'sleep_hours': sleep_hours,
                        },
                        'page_title': 'Prediction Result',
                    }
                    return render(request, 'prediction/result.html', context)
                    
                except Exception as e:
                    messages.error(request, f'Error making prediction: {str(e)}')
            else:
                messages.error(
                    request, 
                    'ML model not found. Please train the model first. '
                    'Run: python train_model.py'
                )
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PredictionForm()
    
    context = {
        'form': form,
        'page_title': 'Predict Weight Loss',
    }
    return render(request, 'prediction/predict.html', context)


def dashboard(request):
    """
    Render the dashboard page with visualizations and model metrics.
    Loads dataset statistics and model performance data.
    """
    dataset_stats = {}
    chart_data = {}
    model_metrics = {}
    
    try:
        # Load dataset for statistics
        dataset_path = settings.DATASET_PATH
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            
            # Basic dataset statistics
            dataset_stats = {
                'total_records': len(df),
                'avg_age': round(df['age'].mean(), 1),
                'avg_weight': round(df['weight_kg'].mean(), 1),
                'avg_workout_hours': round(df['workout_hours_per_week'].mean(), 1),
                'avg_weight_loss': round(df['weight_loss_kg'].mean(), 2),
                'max_weight_loss': round(df['weight_loss_kg'].max(), 2),
                'min_weight_loss': round(df['weight_loss_kg'].min(), 2),
                'male_count': int(df[df['gender'] == 1].shape[0]),
                'female_count': int(df[df['gender'] == 0].shape[0]),
            }
            
            # Chart data: Age distribution
            age_bins = [15, 25, 35, 45, 55, 65]
            age_labels = ['15-24', '25-34', '35-44', '45-54', '55-64']
            age_counts = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False).value_counts().sort_index()
            
            # Chart data: Weight loss by workout hours
            workout_bins = [0, 2, 4, 6, 8, 10]
            workout_labels = ['0-2', '2-4', '4-6', '6-8', '8-10']
            df['workout_bin'] = pd.cut(df['workout_hours_per_week'], bins=workout_bins, labels=workout_labels, right=False)
            avg_loss_by_workout = df.groupby('workout_bin', observed=False)['weight_loss_kg'].mean()
            
            # Chart data: Weight loss by gender
            gender_loss = df.groupby('gender')['weight_loss_kg'].mean()
            
            # Chart data: Calorie intake distribution
            calorie_bins = [1000, 1500, 2000, 2500, 3000]
            calorie_labels = ['1000-1500', '1500-2000', '2000-2500', '2500-3000']
            calorie_counts = pd.cut(df['daily_calorie_intake'], bins=calorie_bins, labels=calorie_labels, right=False).value_counts().sort_index()
            
            # Chart data: Weight loss distribution
            wl_bins = [0, 1, 2, 3, 4, 5]
            wl_labels = ['0-1 kg', '1-2 kg', '2-3 kg', '3-4 kg', '4-5 kg']
            wl_counts = pd.cut(df['weight_loss_kg'], bins=wl_bins, labels=wl_labels, right=False).value_counts().sort_index()
            
            chart_data = {
                # Age distribution
                'age_labels': json.dumps(age_labels),
                'age_data': json.dumps(age_counts.tolist()),
                
                # Weight loss by workout hours
                'workout_labels': json.dumps(workout_labels),
                'workout_loss_data': json.dumps([round(v, 2) for v in avg_loss_by_workout.tolist()]),
                
                # Gender comparison
                'gender_labels': json.dumps(['Female', 'Male']),
                'gender_loss_data': json.dumps([
                    round(gender_loss.get(0, 0), 2),
                    round(gender_loss.get(1, 0), 2)
                ]),
                
                # Calorie distribution
                'calorie_labels': json.dumps(calorie_labels),
                'calorie_data': json.dumps(calorie_counts.tolist()),
                
                # Weight loss distribution
                'wl_labels': json.dumps(wl_labels),
                'wl_data': json.dumps(wl_counts.tolist()),
                
                # Scatter data: workout hours vs weight loss
                'scatter_workout': json.dumps(df['workout_hours_per_week'].tolist()),
                'scatter_weight_loss': json.dumps(df['weight_loss_kg'].tolist()),
            }
        
        # Load model metrics if available
        metrics_path = os.path.join(settings.BASE_DIR, 'ml_model', 'model_metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                model_metrics = json.load(f)
    
    except Exception as e:
        messages.error(request, f'Error loading dashboard data: {str(e)}')
    
    # Get prediction history
    recent_predictions = PredictionRecord.objects.all()[:10]
    
    context = {
        'dataset_stats': dataset_stats,
        'chart_data': chart_data,
        'model_metrics': model_metrics,
        'recent_predictions': recent_predictions,
        'page_title': 'Dashboard',
    }
    return render(request, 'prediction/dashboard.html', context)


def api_predict(request):
    """
    REST API endpoint for weight loss prediction.
    Accepts POST requests with JSON data.
    Returns JSON response with prediction result.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'height_cm', 'weight_kg',
            'workout_hours_per_week', 'daily_calorie_intake', 'sleep_hours'
        ]
        
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {'error': f'Missing required field: {field}'}, 
                    status=400
                )
        
        # Load model
        model, scaler = load_model()
        
        if model is None or scaler is None:
            return JsonResponse(
                {'error': 'ML model not loaded. Please train the model first.'}, 
                status=500
            )
        
        # Prepare input
        input_data = np.array([[
            float(data['age']),
            int(data['gender']),
            float(data['height_cm']),
            float(data['weight_kg']),
            float(data['workout_hours_per_week']),
            float(data['daily_calorie_intake']),
            float(data['sleep_hours']),
        ]])
        
        # Scale and predict
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        predicted_weight_loss = max(0, round(float(prediction), 2))
        
        # Save record
        PredictionRecord.objects.create(
            age=int(data['age']),
            gender=int(data['gender']),
            height_cm=float(data['height_cm']),
            weight_kg=float(data['weight_kg']),
            workout_hours_per_week=float(data['workout_hours_per_week']),
            daily_calorie_intake=float(data['daily_calorie_intake']),
            sleep_hours=float(data['sleep_hours']),
            predicted_weight_loss=predicted_weight_loss,
        )
        
        return JsonResponse({
            'success': True,
            'predicted_weight_loss_kg': predicted_weight_loss,
            'interpretation': get_interpretation(
                predicted_weight_loss,
                float(data['workout_hours_per_week']),
                float(data['daily_calorie_intake'])
            ),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_interpretation(weight_loss, workout_hours, calories):
    """
    Generate a human-readable interpretation of the prediction.
    
    Args:
        weight_loss: Predicted weight loss in kg
        workout_hours: Weekly workout hours
        calories: Daily calorie intake
    
    Returns:
        Dictionary with interpretation details
    """
    interpretation = {
        'level': '',
        'message': '',
        'tips': [],
        'color': '',
    }
    
    if weight_loss >= 4.0:
        interpretation['level'] = 'Excellent'
        interpretation['message'] = (
            'Your predicted weight loss is excellent! '
            'Your workout routine and lifestyle are highly effective.'
        )
        interpretation['color'] = 'success'
    elif weight_loss >= 3.0:
        interpretation['level'] = 'Very Good'
        interpretation['message'] = (
            'Great progress expected! Your fitness plan is working well.'
        )
        interpretation['color'] = 'info'
    elif weight_loss >= 2.0:
        interpretation['level'] = 'Good'
        interpretation['message'] = (
            'Moderate weight loss predicted. There is room for improvement.'
        )
        interpretation['color'] = 'primary'
    elif weight_loss >= 1.0:
        interpretation['level'] = 'Fair'
        interpretation['message'] = (
            'Mild weight loss predicted. Consider increasing your workout intensity.'
        )
        interpretation['color'] = 'warning'
    else:
        interpretation['level'] = 'Low'
        interpretation['message'] = (
            'Minimal weight loss predicted. Significant lifestyle changes recommended.'
        )
        interpretation['color'] = 'danger'
    
    # Generate personalized tips
    if workout_hours < 3:
        interpretation['tips'].append(
            'Increase your workout hours to at least 3-4 hours per week.'
        )
    if workout_hours < 5:
        interpretation['tips'].append(
            'Try adding high-intensity interval training (HIIT) to your routine.'
        )
    if calories > 2200:
        interpretation['tips'].append(
            'Consider reducing your daily calorie intake for better results.'
        )
    if calories < 1500:
        interpretation['tips'].append(
            'Ensure you are eating enough to fuel your workouts properly.'
        )
    
    interpretation['tips'].append('Stay consistent with your workout schedule.')
    interpretation['tips'].append('Drink plenty of water throughout the day.')
    interpretation['tips'].append('Get adequate sleep (7-8 hours) for recovery.')
    
    return interpretation


def get_bmi_category(bmi):
    """
    Determine BMI category based on BMI value.
    
    Args:
        bmi: Body Mass Index value
    
    Returns:
        Dictionary with category name and color
    """
    if bmi < 18.5:
        return {'category': 'Underweight', 'color': 'info'}
    elif bmi < 25:
        return {'category': 'Normal Weight', 'color': 'success'}
    elif bmi < 30:
        return {'category': 'Overweight', 'color': 'warning'}
    else:
        return {'category': 'Obese', 'color': 'danger'}
