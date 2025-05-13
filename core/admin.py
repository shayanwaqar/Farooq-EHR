from django.contrib import admin
from .models import Patient, Visit

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date')

