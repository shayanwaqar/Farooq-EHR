from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('create-patient/', views.create_patient, name='create_patient'),
]
