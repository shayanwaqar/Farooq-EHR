from django.shortcuts import render, redirect
from .models import Patient, Visit
from .forms import PatientSearchForm
from rapidfuzz import fuzz

def volunteer_dashboard(request):
    form = PatientSearchForm()
    match = None
    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            dob = form.cleaned_data['date_of_birth']
            
            # Perform fuzzy match
            best_match = None
            best_score = 0
            for patient in Patient.objects.filter(date_of_birth=dob):
                score = fuzz.ratio(f"{patient.first_name.lower()} {patient.last_name.lower()}",
                                   f"{fname.lower()} {lname.lower()}")
                if score > best_score:
                    best_score = score
                    best_match = patient

            if best_score >= 90:
                match = best_match  # Show match
            else:
                # Redirect to new patient creation with prefilled info
                request.session['new_patient'] = {
                    'first_name': fname,
                    'last_name': lname,
                    'date_of_birth': str(dob)
                }
                return redirect('create_patient')

    return render(request, 'core/volunteer_dashboard.html', {
        'form': form,
        'match': match
    })




####
from django.http import HttpResponse
from django import forms

class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']

def create_patient(request):
    initial_data = request.session.get('new_patient', {})
    form = NewPatientForm(initial=initial_data)
    
    if request.method == 'POST':
        form = NewPatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            del request.session['new_patient']
            return redirect('volunteer_dashboard')

    return render(request, 'core/create_patient.html', {'form': form})
