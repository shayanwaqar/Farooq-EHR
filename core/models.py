from django.db import models
# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField(auto_now_add=True)
    scanned_form = models.FileField(upload_to='scanned_forms/', blank=True, null=True)

    def __str__(self):
        return f"Visit on {self.date} for {self.patient}"

