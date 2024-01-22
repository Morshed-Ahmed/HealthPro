from django.shortcuts import render,redirect
from .models import Doctor,Specialization,Appointment,Review
from .forms import ReviewForm,AppointmentForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def HomeView(request,specialization_name = None):
    data = Doctor.objects.all()
    specialization = Specialization.objects.all()
    if specialization_name == 'all':
        data = Doctor.objects.all()
    elif specialization_name is not None:
        bt = Specialization.objects.get(name = specialization_name)
        # print(data)
        data = Doctor.objects.filter(specialization = bt)
        # print(data)
    return render(request , 'home.html',{'data': data,'specialization':specialization})


def DoctorDetails(request,doctor_id):
    is_appointment = bool
    data = Doctor.objects.get(id = doctor_id)
    review_data = Review.objects.filter(doctor = doctor_id)
    # print('re',review_data)
    try:
        profile = User.objects.get(username=request.user.username)
        appoint = Appointment.objects.filter(patient= profile,doctor= data)
        if len(appoint) > 0:
            is_appointment = True
        else:
            is_appointment = False
    except:
        is_appointment = False

        
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        appointForm = AppointmentForm(request.POST)
        if appointForm.is_valid():
            appointment = appointForm.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = data
            appointment.save()
            messages.success(request,'Appointment Successful.')

            return redirect('doctor_details',data.id)  

        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.doctor = data
            review.save()
            messages.success(request,'Thanks for the review')

            return redirect('doctor_details',data.id)

    else:
        form = ReviewForm()
        appointForm = AppointmentForm()

    return render(request,'doctorDetails.html',{'data':data,'form': form,'appointForm':appointForm,'is_appointment':is_appointment,'review_data':review_data})

def DoctorAppointment(request,doctor_id):
    doctor = Doctor.objects.get(id = doctor_id)
    patient = request.user
    return render(request,'doctorDetails.html' ,{'appointForm':appointForm})