# Telecom Customer Churn Predictor

Django web app that predicts customer churn probability, risk level (Low / Moderate / High)
and a suggested retention action. Model: Logistic Regression (scikit-learn pipeline).

## Run
1. python -m venv venv, then activate it
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py load_customers   (optional: fills the dashboard with sample data)
6. python manage.py runserver, then open http://127.0.0.1:8000/

## Login
Superuser username: shreya
Superuser password: superuser

## Structure
- data/                        : Telco Customer Churn dataset
- notebooks/churn_training.ipynb : preprocessing, training, evaluation
- ml/churn_pipeline.joblib     : trained model
- predictor/                   : Django app (models, forms, views, services, management commands)
- templates/                   : HTML templates (login, predict, result, history, dashboard)

## Pages
- /              : prediction form (login required)
- /result/<pk>/  : single prediction result
- /history/      : list of all predictions
- /dashboard/    : summary cards + risk distribution and contract-type charts
- /admin/        : Django admin (view the Prediction table)

## Note on the dashboard
The dashboard is populated by scoring the training data with the trained model.
Predicted churn rate is therefore not an out-of-sample metric.
