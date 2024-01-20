from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    email = forms.EmailField(widget= forms.EmailInput(attrs={'id':'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
    
    def save(self):
        user = super().save()
        user.is_active = False
        user.save()
        return user