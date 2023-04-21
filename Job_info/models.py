from datetime import date

from django.db import models

# from django.utils import timezone


# Create your models here.
GENDER_CHOICE = (
    ('M', "Male"),
    ('F', "Female"),
    ("Other", "Other")
)

STATE_CHOICE = (
    ('Rj', "Rajasthan"),
    ('Up', "UtterPradesh"),
    ('Mp', "MadhyaPradesh"),
    ('Mh', "Maharashtra"),
    ('Guj', "Gujarat"),
    ('Tn', "Tamilnadu")

)


class Applicant(models.Model):
    # id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=50)
    fullname = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICE, max_length=100)
    mobile = models.CharField(max_length=12, default=None)
    state = models.CharField(choices=STATE_CHOICE, max_length=100)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    #
    # def __str__(self):
    #     return self.company_id


class Company(models.Model):
    # id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.username
    # active_status = models.BooleanField(default=True)


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.FloatField()
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    # creation_date = models.DateTimeField(default=timezone.now)
    creation_date = models.DateTimeField(default=date.today)
    is_approved = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.id


EXPERIENCE_CHOICE = (

    ("Fresher", "Fresher"),
    ("1y", "1 year"),
    ("2y", "2 year"),
    ("3y", "3 year"),
    ("4y", "4 year"),
    ("5y", "5 year"),
    ("above 5y", "above 5 year")

)


class Applications(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    experience = models.CharField(choices=EXPERIENCE_CHOICE, max_length=100)
    photo = models.ImageField(upload_to="ApplicantPhotos", blank=True)
    resume = models.FileField(upload_to="ApplicantResume", blank=True)
    apply_date = models.DateField()

    # def __str__(self):
    # return str(self.applicant)


class AdminPanel(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
