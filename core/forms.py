from django import forms

class PatientSearchForm(forms.Form):
    first_name = forms.CharField(label="*First Name")
    last_name = forms.CharField(label="*Last Name")
    date_of_birth = forms.DateField(required=False, label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
