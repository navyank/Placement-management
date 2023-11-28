from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class State(models.Model):
    state=models.CharField(max_length=50) 
     
    
    def __str__(self):
        return self.state 
class District(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    district=models.CharField(max_length=50)
      
    
        
    def __str__(self):
        return self.district

class Qualification(models.Model):
    qualification=models.CharField(max_length=50)
     
    def __str__(self):
        return self.qualification
class Course(models.Model):
    course=models.CharField(max_length=50)    
    
    def __str__(self):
        return self.course  
class Batch(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    Startdate=models.DateField()
    Enddate=models.DateField()
    Time=models.TimeField()
    batch=models.CharField(max_length=50)    
    
    def __str__(self):
        return self.batch         
class Trainer(models.Model):
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    trainer = models.ManyToManyField(
        User,
        related_name="UserTrainers", blank=True, limit_choices_to={"is_active": True, 'groups__name': 'trainer'},
    ) 
    def __str__(self):
        trainer_usernames = ', '.join([trainer.username for trainer in self.trainer.all()])
        return f"{trainer_usernames}"        
