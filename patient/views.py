from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import forms

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator

from doctor.models import Appointment,Doctor

# Create your views here.
def RegisterView(request):
    if not request.user.is_authenticated:
        form = forms.RegisterForm()
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                confirm_link = f'https://healthpro.onrender.com/account/active/{uid}/{token}'
                email_subject = "Confirm your email"
                email_body = render_to_string(
                    'confirm_email.html',
                    {'confirm_link': confirm_link}
                )
                email = EmailMultiAlternatives(
                    subject=email_subject, body=email_body, to=[user.email]
                )
                email.attach_alternative(email_body, 'text/html')
                email.send()
                messages.success(
                    request, 'Check your email.')
                return redirect('register')
            else:
                messages.error(request, 'Please correct information.')
        else:
            form = forms.RegisterForm()

        return render(request, 'register.html', {'form': form, 'title': 'Sign Up', 'button_text': 'Sign Up', 'button_class': 'btn-success'})
    else:
        return redirect('home')

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # patients = models.Patient.objects.get(user=user)
        # patients.is_patient = True
        # patients.save()
        # messages.success(request,'Email verify Successful')

        return redirect('login')
    else:
        return redirect('register')


# def RegisterView(request):
#     if request.method == 'POST':
#         form = forms.RegisterForm(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Account created successfully')
#             # form.save()
#             print(form.cleaned_data)
#     else:
#         form = forms.RegisterForm()
#     return render(request, 'register.html', {'form': form})
def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    # messages.success(request, 'Logged In Successfully')
                    messages.info(
                        request, f"You are now logged in as {username}")

                    # Redirect to the appropriate page after login
                else:
                    messages.error(request, 'Invalid username or password')

        else:
            form = AuthenticationForm()

        return render(request, 'login.html', {'form': form,})
    else:
        return redirect('home')


def UserLogout(request):
    logout(request)
    # messages.info(request, "Logged Out Successfully")
    return redirect('home')

def ProfileView(request):
    is_doctor = bool

    try:
        kk = Doctor.objects.get(user= request.user)
        print('kk',kk)
        is_doctor = True
    except:
        is_doctor = False
    print('pp',is_doctor)

    if is_doctor:
        appoint_data = Appointment.objects.filter(doctor = kk)
        is_doctor = True
    else:
        appoint_data = Appointment.objects.filter(patient = request.user)
        is_doctor = False
    print(appoint_data)
    return render(request,'profile.html',{'appoint_data':appoint_data,'is_doctor':is_doctor})