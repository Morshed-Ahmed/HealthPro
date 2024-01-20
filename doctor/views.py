from django.shortcuts import render,redirect
from .models import Doctor,Specialization
from .forms import ReviewForm,AppointmentForm
# Create your views here.
def HomeView(request,specialization_name = None):
    data = Doctor.objects.all()
    specialization = Specialization.objects.all()
    if specialization_name == 'all':
        data = Doctor.objects.all()
    elif specialization_name is not None:
        bt = Specialization.objects.get(name = specialization_name)
        print(data)
        data = Doctor.objects.filter(specialization = bt)
        print(data)
    return render(request , 'home.html',{'data': data,'specialization':specialization})


def DoctorDetails(request,doctor_id):
    data = Doctor.objects.get(id = doctor_id)
    form = ReviewForm()
    if request.method == 'POST':
        appointForm = AppointmentForm(request.POST)
        if appointForm.is_valid():
            appointment = appointForm.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = data
            appointment.save()

            
            return redirect('doctor_details')  
    else:
        appointForm = AppointmentForm()
 


    return render(request,'doctorDetails.html',{'data':data,'form': form,'appointForm':appointForm})

def DoctorAppointment(request,doctor_id):
    doctor = Doctor.objects.get(id = doctor_id)
    patient = request.user
    return render(request,'doctorDetails.html' ,{'appointForm':appointForm})