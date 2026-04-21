# 🏋️ Gym Weight Loss Prediction System

A complete Django web application integrated with a Machine Learning model to predict weight loss outcomes for gym members based on their workout and lifestyle data.

## 📁 Project Structure

```
GYM_project/
├── gym_project/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── prediction/                  # Django prediction app
│   ├── __init__.py
│   ├── admin.py                 # Admin panel configuration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # Form definitions
│   ├── models.py                # Database models
│   ├── urls.py                  # App URL patterns
│   └── views.py                 # View functions
├── templates/                   # HTML templates
│   └── prediction/
│       ├── base.html            # Base template
│       ├── home.html            # Home page
│       ├── about.html           # About page
│       ├── predict.html         # Prediction form page
│       ├── result.html          # Prediction result page
│       └── dashboard.html       # Analytics dashboard
├── static/                      # Static files
│   ├── css/
│   │   └── style.css            # Custom CSS styles
│   └── images/                  # Generated chart images
├── data/                        # Dataset directory
│   └── gym_members_dataset.csv  # Sample dataset
├── ml_model/                    # Trained ML model files
│   ├── weight_loss_model.pkl    # Trained model
│   ├── scaler.pkl               # Feature scaler
│   └── model_metrics.json       # Model performance metrics
├── notebooks/                   # Jupyter notebooks
│   └── gym_weight_loss_analysis.ipynb
├── manage.py                    # Django management script
├── train_model.py               # Model training script
├── create_notebook.py           # Notebook generator helper
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone/Navigate to the Project
```bash
cd GYM_project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the ML Model
```bash
python train_model.py
```
This will:
- Load the dataset from `data/gym_members_dataset.csv`
- Train multiple regression models
- Select the best performing model
- Save the model to `ml_model/weight_loss_model.pkl`
- Save the scaler to `ml_model/scaler.pkl`
- Save metrics to `ml_model/model_metrics.json`

### Step 5: Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Run the Django Server
```bash
python manage.py runserver
```

### Step 8: Access the Application
- **Home Page**: http://127.0.0.1:8000/
- **Prediction Page**: http://127.0.0.1:8000/predict/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **About Page**: http://127.0.0.1:8000/about/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📓 Running the Jupyter Notebook

### Step 1: Install Jupyter (if not already installed)
```bash
pip install jupyter notebook
```

### Step 2: Launch Jupyter Notebook
```bash
cd notebooks
jupyter notebook
```

### Step 3: Open the Notebook
Open `gym_weight_loss_analysis.ipynb` in the Jupyter interface and run all cells sequentially.

The notebook includes:
- Data loading and exploration
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA) with visualizations
- Feature selection and importance analysis
- Model training (Linear Regression, Random Forest, Gradient Boosting, SVR)
- Model evaluation and comparison
- Model export (saves .pkl files)

## 🔧 Technology Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.x | Core programming language |
| Django 4.2+ | Web framework |
| SQLite | Database |
| scikit-learn | Machine Learning |
| pandas | Data manipulation |
| numpy | Numerical computing |
| matplotlib | Data visualization |
| seaborn | Statistical visualization |
| Bootstrap 5 | Frontend CSS framework |
| Chart.js | Interactive charts |
| Jupyter Notebook | ML development |

## 📊 Features

1. **Home Page** - Project overview with animated hero section
2. **About Page** - Project objectives, methodology, and technology stack
3. **Prediction Page** - Interactive form with real-time BMI calculation
4. **Result Page** - Predicted weight loss with interpretation and recommendations
5. **Dashboard** - Interactive charts and model performance metrics
6. **Admin Panel** - Manage users and prediction records
7. **REST API** - JSON endpoint for programmatic predictions

## 🔌 REST API

### Endpoint: `POST /api/predict/`

**Request Body (JSON):**
```json
{
    "age": 25,
    "gender": 1,
    "height_cm": 175,
    "weight_kg": 85,
    "workout_hours_per_week": 5,
    "daily_calorie_intake": 2200,
    "sleep_hours": 7
}
```

**Response:**
```json
{
    "success": true,
    "predicted_weight_loss_kg": 3.2,
    "interpretation": {
        "level": "Very Good",
        "message": "Great progress expected!",
        "tips": ["..."],
        "color": "info"
    }
}
```

## 📈 ML Model Details

- **Algorithm**: Random Forest Regressor (best performer)
- **Features**: age, gender, height, weight, workout hours, calorie intake, sleep hours
- **Target**: Weight loss (kg)
- **Preprocessing**: StandardScaler for feature normalization
- **Evaluation Metrics**: R², MAE, MSE, RMSE

## 📝 Notes

- The dataset contains synthetic data for demonstration purposes
- Gender is encoded as: Male = 1, Female = 0
- The model predicts weight loss in kilograms
- Ensure the ML model is trained before running the Django server
- The admin panel requires a superuser account

## 📄 License

This project is for educational purposes.
