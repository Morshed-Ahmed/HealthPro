from django import forms
from .models import Review,Appointment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body','rating',]

class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        fields = ['time','symptom']