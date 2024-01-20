from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView,name = 'home'),
    path('specialization/<str:specialization_name>/',views.HomeView, name = 'sp_wise_product'),
    path('doctor_details/<int:doctor_id>/',views.DoctorDetails,name = 'doctor_details'),
    path('appointment/<int:doctor_id>/',views.DoctorAppointment, name = 'appointment'),

]
