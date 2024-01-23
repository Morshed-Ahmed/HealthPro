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
                    request, ' Please check your email.')
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
        messages.success(request,'Email verify Successful, Please Login')
        return redirect('login')
    else:
        return redirect('register')

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

                    messages.info(
                        request, f"You are now logged in as {username}")
                    return redirect('profile')

                else:
                    messages.info(request, 'Invalid username or password')
            else:
                messages.info(request, 'Invalid username or password')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form,})
    else:
        return redirect('home')


def UserLogout(request):
    logout(request)
    messages.info(request, "LogOut Successfully")
    return redirect('login')

def ProfileView(request):
    is_doctor = bool
    try:
        kk = Doctor.objects.get(user= request.user)
        # print('kk',kk)
        is_doctor = True
    except:
        is_doctor = False
    # print('pp',is_doctor)

    if is_doctor:
        appoint_data = Appointment.objects.filter(doctor = kk)
        is_doctor = True
    else:
        appoint_data = Appointment.objects.filter(patient = request.user)
        is_doctor = False
    # print(appoint_data)
    updateds = forms.AppointmentStatusForm()


    return render(request,'profile.html',{'appoint_data':appoint_data,'is_doctor':is_doctor,'updateds':updateds})


def CancelAppointment(request,appointment_id):
    appoint = Appointment.objects.get(id = appointment_id)
    appoint.delete()
    messages.info(request, "Appointment deleted Successfully")
    return redirect('profile')

# def UpdateAppointment(request,appointment_id):
#     print('id',appointment_ids)
#     appoint = Appointment.objects.get(id = appointment_ids)
#     selected_status = request.POST.get('selected_status')
#     print('stt',selected_status)

#     if request.method == 'POST':
#         # Get the selected status from the form data
#         selected_status = request.POST.get('selected_status')

#         if selected_status:
#             appoint.appointment_status = selected_status
#             appoint.save()
#             messages.success(request, 'Appointment status updated successfully!')
#         else:
#             messages.error(request, 'Error updating appointment status. Please provide a valid status.')


#     return redirect('profile')

def UpdateAppointment(request,appointment_id):
    # print(appointment_id)
    appoint = Appointment.objects.get(id = appointment_id)

    if request.method == 'POST':
        form = forms.AppointmentStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['appointment_status']
            appoint.appointment_status = status
            appoint.save()
            messages.success(request, 'Appointment status updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating appointment status. Please provide a valid status.')
    else:
        form = forms.AppointmentStatusForm()

    return render(request,'confirm_appoint_update.html',{'appoint':form})