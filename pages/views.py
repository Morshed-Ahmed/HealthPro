from django.shortcuts import render
from doctor.models import Doctor,Specialization,Review

# Create your views here.

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def DoctorsView(request,specialization_name = None):
    data = Doctor.objects.all()
    specialization = Specialization.objects.all()
    review = Review.objects.all()
    if specialization_name == 'all':
        data = Doctor.objects.all()
    elif specialization_name is not None:
        bt = Specialization.objects.get(name = specialization_name)
        # print(data)
        data = Doctor.objects.filter(specialization = bt)
        # print(data)
    return render(request , 'doctors.html',{'data': data,'specialization':specialization,'review':review})


def AboutView(request):
    return render(request, 'about.html')
    
def ContactView(request):
    return render(request, 'contact.html')

def BlogView(request):
    return render(request, 'blog.html')