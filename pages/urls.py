from django.urls import path
from . import views
from django.conf.urls import handler404



urlpatterns = [
    path('doctors/',views.DoctorsView, name = 'doctors'),
    path('specialization/<str:specialization_name>/',views.DoctorsView, name = 'sp_wise_doctor'),
    path('about-us',views.AboutView, name = 'about-us'),
    path('contact-us',views.ContactView, name = 'contact-us'),
    path('blog',views.BlogView, name = 'blog'),
]

handler404 = views.custom_404
