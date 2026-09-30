from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_view, name='predict'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
