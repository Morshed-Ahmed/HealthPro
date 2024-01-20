from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Specialization(models.Model):
    name = models.CharField(max_length = 30)
    slug = models.SlugField(max_length = 40)
    def __str__(self):
        return self.name
class Designation(models.Model):
    name = models.CharField(max_length = 30)
    slug = models.SlugField(max_length = 40)
    def __str__(self):
            return self.name
class AvailableTime(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="doctor/images/")
    designation = models.ManyToManyField(Designation)
    specialization =  models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    fee = models.IntegerField()
    # meet_link = models.CharField(max_length = 100)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


APPOINTMENT_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Running', 'Running'),
]

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    appointment_status = models.CharField(choices = APPOINTMENT_STATUS, max_length = 10, default = "Pending")
    symptom = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete = models.CASCADE)
    cancel = models.BooleanField(default = False)
    
    # def __str__(self):
    #     return f"Doctor : {self.doctor.user.first_name} , Patient : {self.patient.user.first_name}"
    


STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10 , blank = True, null = True)
    
    def __str__(self):
        return f"Patient : {self.reviewer.user.first_name} ; Doctor {self.doctor.user.first_name}"