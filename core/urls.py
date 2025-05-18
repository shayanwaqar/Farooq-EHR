from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('check-in/<int:patient_id>/', views.check_in_patient, name='check_in_patient'),
    path('upload/<int:patient_id>/', views.upload_visit_form, name='upload_visit_form'),
    path('create-patient/', views.create_patient, name='create_patient'),  # ✅ This is the fix
    path('remove-from-queue/<int:visit_id>/', views.remove_from_queue, name='remove_from_queue'),
]