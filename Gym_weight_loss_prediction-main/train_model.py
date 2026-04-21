"""
Model Training Script for Gym Weight Loss Prediction System.

This script trains a machine learning model to predict weight loss
based on gym members' workout and lifestyle data.

Usage:
    python train_model.py

Output:
    - ml_model/weight_loss_model.pkl (trained model)
    - ml_model/scaler.pkl (feature scaler)
    - ml_model/model_metrics.json (performance metrics)
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score
)
import joblib
import warnings
warnings.filterwarnings('ignore')


def load_and_preprocess_data(filepath):
    """
    Load and preprocess the gym members dataset.
    
    Args:
        filepath: Path to the CSV dataset file.
    
    Returns:
        Tuple of (X, y, feature_names) where X is the feature matrix,
        y is the target vector, and feature_names is a list of feature names.
    """
    print("=" * 60)
    print("STEP 1: Loading and Preprocessing Data")
    print("=" * 60)
    
    # Load dataset
    df = pd.read_csv(filepath)
    print(f"\nDataset loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    # Check for missing values
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
    # Dataset statistics
    print(f"\nDataset Statistics:")
    print(df.describe())
    
    # Define features and target
    feature_names = [
        'age', 'gender', 'height_cm', 'weight_kg',
        'workout_hours_per_week', 'daily_calorie_intake', 'sleep_hours'
    ]
    target = 'weight_loss_kg'
    
    X = df[feature_names].values
    y = df[target].values
    
    print(f"\nFeatures: {feature_names}")
    print(f"Target: {target}")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
    
    return X, y, feature_names


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Train multiple regression models and evaluate their performance.
    
    Args:
        X_train, X_test: Training and testing feature matrices.
        y_train, y_test: Training and testing target vectors.
    
    Returns:
        Dictionary of model results with metrics.
    """
    print("\n" + "=" * 60)
    print("STEP 3: Training and Evaluating Models")
    print("=" * 60)
    
    # Define models to evaluate
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(
            n_estimators=100, 
            random_state=42,
            max_depth=10,
            min_samples_split=5
        ),
        'Gradient Boosting': GradientBoostingRegressor(
            n_estimators=100, 
            random_state=42,
            max_depth=5,
            learning_rate=0.1
        ),
        'SVR': SVR(kernel='rbf', C=100, gamma='scale'),
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'mae': round(mae, 4),
            'mse': round(mse, 4),
            'rmse': round(rmse, 4),
            'r2': round(r2, 4),
        }
        
        print(f"  MAE:  {mae:.4f}")
        print(f"  MSE:  {mse:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²:   {r2:.4f}")
    
    return results


def select_best_model(results):
    """
    Select the best model based on R² score.
    
    Args:
        results: Dictionary of model results.
    
    Returns:
        Tuple of (best_model_name, best_model, best_metrics).
    """
    print("\n" + "=" * 60)
    print("STEP 4: Selecting Best Model")
    print("=" * 60)
    
    best_name = max(results, key=lambda k: results[k]['r2'])
    best_result = results[best_name]
    
    print(f"\n[BEST] Best Model: {best_name}")
    print(f"   R2 Score: {best_result['r2']}")
    print(f"   MAE: {best_result['mae']}")
    print(f"   RMSE: {best_result['rmse']}")
    
    return best_name, best_result['model'], best_result


def save_model(model, scaler, best_name, best_metrics, output_dir='ml_model'):
    """
    Save the trained model, scaler, and metrics to disk.
    
    Args:
        model: Trained ML model.
        scaler: Fitted StandardScaler.
        best_name: Name of the best model.
        best_metrics: Dictionary of performance metrics.
        output_dir: Directory to save files.
    """
    print("\n" + "=" * 60)
    print("STEP 5: Saving Model and Artifacts")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, 'weight_loss_model.pkl')
    joblib.dump(model, model_path)
    print(f"\n[OK] Model saved to: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"[OK] Scaler saved to: {scaler_path}")
    
    # Save metrics
    metrics = {
        'best_model': best_name,
        'r2_score': best_metrics['r2'],
        'mae': best_metrics['mae'],
        'mse': best_metrics['mse'],
        'rmse': best_metrics['rmse'],
    }
    
    metrics_path = os.path.join(output_dir, 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"[OK] Metrics saved to: {metrics_path}")
    
    return metrics


def main():
    """Main function to orchestrate the model training pipeline."""
    print("\n" + "=" * 60)
    print("  GYM WEIGHT LOSS PREDICTION - MODEL TRAINING")
    print("=" * 60)
    
    # File paths
    dataset_path = os.path.join('data', 'gym_members_dataset.csv')
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"\n[ERROR] Dataset not found at '{dataset_path}'")
        print("Please ensure the dataset file exists.")
        return
    
    # Step 1: Load and preprocess data
    X, y, feature_names = load_and_preprocess_data(dataset_path)
    
    # Step 2: Split data and scale features
    print("\n" + "=" * 60)
    print("STEP 2: Splitting Data and Scaling Features")
    print("=" * 60)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Features scaled using StandardScaler.")
    
    # Step 3: Train and evaluate models
    results = train_and_evaluate_models(
        X_train_scaled, X_test_scaled, y_train, y_test
    )
    
    # Step 4: Select best model
    best_name, best_model, best_metrics = select_best_model(results)
    
    # Step 5: Save model and artifacts
    metrics = save_model(best_model, scaler, best_name, best_metrics)
    
    # Summary
    print("\n" + "=" * 60)
    print("  TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\n[MODEL] Model: {best_name}")
    print(f"[SCORE] R2 Score: {metrics['r2_score']}")
    print(f"[SCORE] MAE: {metrics['mae']}")
    print(f"[SCORE] RMSE: {metrics['rmse']}")
    print(f"\n[NEXT] You can now run the Django server:")
    print(f"   python manage.py runserver")
    print("=" * 60)


if __name__ == '__main__':
    main()
