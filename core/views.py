from datetime import date
from django.shortcuts import render, redirect
from .models import Patient, Visit
from .forms import PatientSearchForm
from rapidfuzz import fuzz

def volunteer_dashboard(request):
    form = PatientSearchForm()
    match = None
    score = 0

    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name'].strip().lower()
            lname = form.cleaned_data['last_name'].strip().lower()
            dob = form.cleaned_data['date_of_birth']

            candidates = Patient.objects.filter(date_of_birth=dob)
            best_score = 0
            best_match = None

            for patient in candidates:
                p_fname = patient.first_name.strip().lower()
                p_lname = patient.last_name.strip().lower()

                s = fuzz.ratio(fname + lname, p_fname + p_lname)
                if s > best_score:
                    best_score = s
                    best_match = patient

            if best_score >= 85:
                match = best_match
                score = best_score

    return render(request, 'core/volunteer_dashboard.html', {
        'form': form,
        'match': match,
        'score': score,
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


def check_in_patient(request, patient_id):
    if request.method == "POST":
        patient = Patient.objects.get(id=patient_id)
        Visit.objects.create(patient=patient, date=date.today())
        return redirect('upload_visit_form', patient_id=patient.id)
    
def upload_visit_form(request, patient_id):
    return HttpResponse(f"Upload page for patient {patient_id}")
