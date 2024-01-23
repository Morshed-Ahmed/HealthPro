from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView,name = 'register'),
    path('login/',views.LoginView,name = 'login'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('logout/',views.UserLogout,name = 'logout'),
    path('profile/',views.ProfileView,name = 'profile'),
    path('cancel_appointment/<int:appointment_id>/',views.CancelAppointment,name = 'cancel_appointment'),
    path('update_appointment/<int:appointment_id>/',views.UpdateAppointment,name = 'update_appointment'),
]
