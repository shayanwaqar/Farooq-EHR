from datetime import date
import math
from django.shortcuts import render, redirect
from .models import Patient, Visit
from .forms import PatientSearchForm
from rapidfuzz import fuzz
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.views.decorators.http import require_POST


def volunteer_dashboard(request):
    form = PatientSearchForm()
    matches = []

    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name'].strip().lower()
            lname = form.cleaned_data['last_name'].strip().lower()

            candidates = Patient.objects.all()
            threshold = 70  # you can tweak this
            for patient in candidates:
                p_fname = patient.first_name.strip().lower()
                p_lname = patient.last_name.strip().lower()
                score = fuzz.ratio(fname + lname, p_fname + p_lname)
                score = round(score)

                if score >= threshold:
                    matches.append((patient, score))

            # Sort by best match score
            matches.sort(key=lambda x: x[1], reverse=True)
            matches = matches[:5] #limited to 5 potential matches.
    
    today = date.today()
    queue = Visit.objects.filter(date=today, in_queue=True).select_related('patient')

    return render(request, 'core/volunteer_dashboard.html', {
        'form': form,
        'matches': matches,
        'queue': queue,
    })


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
        patient = get_object_or_404(Patient, id=patient_id)
        today = date.today()

        # Get or create today's visit
        visit, created = Visit.objects.get_or_create(patient=patient, date=today)

        # Ensure they're in the queue
        visit.in_queue = True
        visit.save()

        return redirect('volunteer_dashboard')
      

@require_POST
def remove_from_queue(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.in_queue = False
    visit.save()
    return redirect('volunteer_dashboard')



def upload_visit_form(request, patient_id):
    return HttpResponse(f"Upload page for patient {patient_id}")

