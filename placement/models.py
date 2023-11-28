from django.db import models
from placementapp.models import *
from studentapp.models import *
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class Company(models.Model):
    Name=models.CharField(max_length=50)
    email_id=models.CharField(max_length=50)
    website=models.CharField(max_length=50)
    state=models.ForeignKey(State,on_delete=models.CASCADE)  
    district=ChainedForeignKey(District,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        sort=True) 
    Phone_Number=models.CharField(max_length=50) 
    contact_person=models.CharField(max_length=50)
    
    def __str__(self):
        return self.Name           

class Job(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    Job_title=models.CharField(max_length=50)
    jobcode=models.CharField(max_length=200)
    Vacancies=models.CharField(max_length=50)
    job_location=models.CharField(max_length=50)     
    MY_GENDER = (("male","Male"), ("female","Female"), ("others","Others"), ("both","both"))
    gender=models.CharField(max_length=300,choices=MY_GENDER,verbose_name="Gender")
    description=models.CharField(max_length=50)
    Course=models.ForeignKey(Course,on_delete=models.CASCADE)
    Salary=models.CharField(max_length=50)
    Last_date=models.DateField()
    
    def __str__(self):
        return self.jobcode  
