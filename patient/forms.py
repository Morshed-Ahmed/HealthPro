from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from doctor.models import Appointment

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    email = forms.EmailField(widget= forms.EmailInput(attrs={'id':'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
    
    def save(self):
        user = super().save()
        user.is_active = False
        user.save()
        return user

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_status']